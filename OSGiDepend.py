#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re,sys,pyyed,argparse

outputHeader = ["Name", "Version", "Number of Dependencies", "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
csvSeparator = "\t"
listSeparator = ", " 
defaultIgnoredPathSegments = ["bin", "target", "examples", "test"]
white = "#FFFFFF"
red = "#FF0000"
green = "#00DB43"
version = '%(prog)s 1.0'
minNodeSize = 50
maxNodeSize = 200

idForNames = dict()
namesForId = dict()
ignoredPathSegments = []
nodeId = 0
time = 0 

def scanForBundles(directory, ignoredPathSegments):
    bundels = set()
    for dirpath, dirNames, files in os.walk(directory):
        ignored = any(ignoredSegment in dirpath for ignoredSegment in ignoredPathSegments)
        if not ignored: 
            for file in files:
                if file == "MANIFEST.MF": 
                    bundels.add(os.path.dirname(dirpath))
    return bundels

def parseBundle(bundlePath):
    manifestPath = bundlePath + "/META-INF/MANIFEST.MF"
    symbolicName, version, exportedPackages, importedPackages, requiredBundles = parseManifest(manifestPath)
    numberOfDependencies = len(requiredBundles)+len(importedPackages)
    bundle = Bundle(bundlePath, symbolicName, version, exportedPackages, importedPackages, requiredBundles, numberOfDependencies)
    return bundle

def parseManifest(manifestPath):
    manifestContent = open(manifestPath, 'rb').read().decode()
    entries = re.split(r'[\r\n]+(?!\s)',manifestContent)
    requiredBundles = []
    importedPackages = []
    exportedPackages = []
    version = ""
    symbolicName = ""
    for entry in entries: 
        if entry.startswith("Require-Bundle:"):
            requiredBundles = [trim(bundle) for bundle in splitEntries(entry,"Require-Bundle:")]
        elif entry.startswith("Import-Package:"):
            importedPackages = [trim(package) for package in splitEntries(entry,"Import-Package:")]
        elif entry.startswith("Export-Package:"):
            # removes 'uses' declaration
            if ';' in entry: entry = entry[:entry.index(';')]
            exportedPackages = [trim(package) for package in splitEntries(entry,"Export-Package:")]
        elif entry.startswith("Bundle-Version:"):
            version = trim(entry.replace("Bundle-Version:", ""))
        elif entry.startswith("Bundle-SymbolicName:"):
            symbolicName = trim(entry.replace("Bundle-SymbolicName:", ""))
            if ";" in symbolicName:
                symbolicName = symbolicName[:symbolicName.index(";")]
    # remove additional information
    requiredBundles[:] = [requiredBundle[:requiredBundle.index(";")]  if ";" in requiredBundle else requiredBundle for requiredBundle in requiredBundles]
    return symbolicName, version, exportedPackages, importedPackages, requiredBundles

def trim(str):
    return str.replace("\n","").replace("\r","").strip(" ")

def splitEntries(entry, entryName):
    return re.split(r",(?!\d)", entry.replace(entryName, ""))

def createDependencyGraph(bundles, bundlesForExports):
    graph = pyyed.Graph()
    bundleNames = [bundle.name for bundle in bundles]
    numDependencies = [bundle.numberOfDependencies for bundle in bundles]
    numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
    for bundle in bundles:
        ignored = any(ignoredSegment in bundle.path for ignoredSegment in ignoredPathSegments)
        if not ignored:
            nodeSize = interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
            addNode(bundle.name, graph, width=str(nodeSize), height=str(nodeSize))
            for reqBundle in bundle.requiredBundles:
                ignored = any(ignoredSegment in reqBundle for ignoredSegment in ignoredPathSegments)
                if not ignored:
                    if reqBundle in bundleNames: 
                        nodeSize = interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                        addNode(reqBundle, graph, width=str(nodeSize), height=str(nodeSize))
                    elif addNode(reqBundle, graph, color=white): 
                        print ("Bundle %s is not contained in workspace." % reqBundle)
                    graph.add_edge(idForNames[bundle.name], idForNames[reqBundle], label="requires")
            for importedPackage in bundle.importedPackages:
                addEdgeForPackageImport(bundle.name, importedPackage, bundlesForExports, numDependenciesForBundle, graph)
    return graph

def interpolateLinear(numDependencies, maxNumDependencies):
    divisor = maxNumDependencies if maxNumDependencies > 0 else 1
    result = (numDependencies / divisor) * (maxNodeSize - minNodeSize) + minNodeSize
    return round(result,0)

def addEdgeForPackageImport(sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle, graph):
    if importedPackage in bundlesForExports:
        exportingBundle = bundlesForExports[importedPackage]
        ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in ignoredPathSegments)
        if not ignored: 
            nodeSize = interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
            addNode(exportingBundle.name, graph, width=str(nodeSize), height=str(nodeSize))
            graph.add_edge(idForNames[sourceBundle], idForNames[exportingBundle.name], label="imports "+importedPackage)
    else:
        ignored = any(ignoredSegment in importedPackage for ignoredSegment in ignoredPathSegments)
        if not ignored: 
            if addNode(importedPackage, graph, color=white, shape="rectangle"):
                print ("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
            graph.add_edge(idForNames[sourceBundle], idForNames[importedPackage], label="imports")

def addNode(bundleName, graph, shape="ellipse", width="50", height="50", color=green):
    global nodeId
    if bundleName not in idForNames:
        idForNames[bundleName] = str(nodeId)
        namesForId[nodeId] = bundleName
        graph.add_node(str(nodeId), label=bundleName, shape=shape, width=width, height=height, shape_fill=color)
        nodeId += 1
        return True
    return False

def mapBundlesOnExports(bundles):
    bundlesForExports = {}
    for bundle in bundles:
        for export in bundle.exportedPackages:
            bundlesForExports[export] = bundle
    return bundlesForExports

def findCyclesRecursive(graph, node, low, disc, stackMember, st,cycles):
    global time 
    disc[node] = time
    low[node] = time
    time += 1
    stackMember[node] = True
    st.append(node)
    adjacentNodes = list([int(edge.node2) for edge in graph.edges.values() if int(edge.node1) == node])
    for adjacent in adjacentNodes:
        if disc[adjacent] == -1 :
            findCyclesRecursive(graph,adjacent, low, disc, stackMember, st,cycles)
            low[node] = min(low[node], low[adjacent])
        elif stackMember[adjacent] == True: 
            low[node] = min(low[node], disc[adjacent])
    # head node found, pop the stack and add SSC
    w = -1
    if low[node] == disc[node]:
        cycle = []
        while w != node:
            w = st.pop()
            cycle.append(w)
            stackMember[w] = False
        cycles.append(cycle)

#The function to do DFS traversal. 
def findCycles(graph):
    numNodes = len(graph.nodes)
    disc = [-1] * (numNodes)
    low = [-1] * (numNodes)
    stackMember = [False] * (numNodes)
    st =[]
    cycles = []
    for node in range(0,numNodes):
        if disc[node] == -1:
            cycles.append(findCyclesRecursive(graph, node, low, disc, stackMember, st, cycles))
    return [cycle for cycle in cycles if None != cycle and len(cycle) > 1]

def markCycles(cycles, graph):
    for cycle in cycles:
        for nodeId in cycle:
            node = graph.nodes[str(nodeId)]
            setattr(node, "shape_fill", red)
            for edge in graph.edges.values():
                fromNode = int(getattr(edge, "node1"))
                toNode = int(getattr(edge, "node2"))
                if fromNode in cycle and toNode in cycle:
                    setattr(edge, "color", red)

def writeCyclesToTxt(path, cylces, graph):
    with open(path, 'w') as outputFile:
        for cycle in cycles: 
            cycleList = listSeparator.join(sorted([graph.nodes[str(nodeId)].label for nodeId in cycle]))
            outputFile.write(cycleList+"\n")

def writeBundlesToCsv(path, bundles):
   with open(path, 'w') as outputFile:
        outputFile.write(csvSeparator.join(outputHeader)+"\n")
        for bundle in sorted(sorted(bundles, key=lambda x: x.name),key=lambda x: x.numberOfDependencies, reverse=True):
            outputFile.write(csvSeparator.join([bundle.name, bundle.version, str(bundle.numberOfDependencies), listSeparator.join(bundle.exportedPackages), listSeparator.join(bundle.importedPackages), listSeparator.join(bundle.requiredBundles), bundle.path])+"\n")

def writeGraphToGraphMl(path, graph):
    with open(path, 'w') as outputFile:
        outputFile.write(graph.get_graph())


class Bundle:
    def __init__(self, path, name, version, exportedPackages, importedPackages, requiredBundles, numberOfDependencies):
        self.path = path.strip(" ")
        self.name = name.strip(" ")
        self.version = version.strip(" ")
        self.exportedPackages = exportedPackages
        self.importedPackages = importedPackages
        self.requiredBundles = requiredBundles
        self.numberOfDependencies = numberOfDependencies
    def __repr__(self):
        return " ".join([self.path, self.name])
    def __lt__(self, other):
        return self.numberOfDependencies < other.numberOfDependencies and self.name < other.name
    def __hash__(self):
        return (self.name.lower()+self.version).__hash__()
    def __eq__(self, other):
        return self.name.lower() == other.name.lower() and self.version == other.version

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workingDir', default=os.getcwd(), help='Root folder for recursive analysis. Default is the script location')
    parser.add_argument('-i', dest='ignoredPathSegments', default=defaultIgnoredPathSegments, help="List of ignored sub path segements of the root location. Default is "+listSeparator.join(defaultIgnoredPathSegments)+". Provide empty list to include all paths", nargs='*' )
    parser.add_argument('-v','--version', action='version', version=version)
    args = parser.parse_args()
    workingDir = args.workingDir
    ignoredPathSegments = args.ignoredPathSegments
    print("Ignoring directory path which contain one of the following strings %s" % ignoredPathSegments)
    print("Scanning for bundles in directory %s..." % workingDir)
    bundlePaths = scanForBundles(workingDir, ignoredPathSegments)
    bundles = [parseBundle(bundle) for bundle in bundlePaths]
    print("Found %d bundle(s)"%len(bundles))
    print("Creating dependency graph...")
    bundlesForExports = mapBundlesOnExports(bundles)
    graph = createDependencyGraph(bundles, bundlesForExports)
    print("Created dependency graph containing %d node(s) and %d edge(s)" % (len(graph.nodes), len(graph.edges)))
    print("Searching for cycles...")
    cycles = findCycles(graph)
    markCycles(cycles, graph)
    print("Found %d cycle(s)" % len(cycles))
    print("Writing output to %s" % str(workingDir))
    writeCyclesToTxt(os.path.join(workingDir,"bundle_cycles.txt"), cycles, graph)
    writeBundlesToCsv(os.path.join(workingDir,"bundles.csv"), bundles)
    writeGraphToGraphMl(os.path.join(workingDir,"dependencies.graphml"), graph)
