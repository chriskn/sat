#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re,sys,pyyed,argparse

outputHeader = ["Name", "Version", "Number of Dependencies", "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
csvSeparator = "\t"
listSeparator = ", " 
defaultIgnoredPathSegments = ["bin", "target", "examples", "test"]
version = '%(prog)s 1.0'
ignoredPathSegments = []




def writeCyclesToTxt(path, cylces, graph):
    with open(path, 'w') as outputFile:
        for cycle in cycles: 
            cycleList = listSeparator.join(sorted([graph.getNodes()[str(nodeId)].label for nodeId in cycle]))
            outputFile.write(cycleList+"\n")

def writeBundlesToCsv(path, bundles):
   with open(path, 'w') as outputFile:
        outputFile.write(csvSeparator.join(outputHeader)+"\n")
        for bundle in sorted(sorted(bundles, key=lambda x: x.name),key=lambda x: x.numberOfDependencies, reverse=True):
            outputFile.write(csvSeparator.join([bundle.name, bundle.version, str(bundle.numberOfDependencies), listSeparator.join(bundle.exportedPackages), listSeparator.join(bundle.importedPackages), listSeparator.join(bundle.requiredBundles), bundle.path])+"\n")

def writeGraphToGraphMl(path, graph):
    with open(path, 'w') as outputFile:
        outputFile.write(graph.serialize())

class BundleGraph:

    graph = None 
    nodeId = 0
    time = 0
    white = "#FFFFFF"
    red = "#FF0000"
    green = "#00DB43"
    minNodeSize = 50
    maxNodeSize = 200
    idForNames = dict()
    namesForId = dict()
    
    def __init__(self, bundles, bundlesForExports):
        self.bundles = bundles
        self.bundlesForExports = bundlesForExports
        self.createDependencyGraph()
        
    def createDependencyGraph(self):
        self.graph = pyyed.Graph()
        self.nodeId = 0
        self.time = 0 
        bundleNames = [bundle.name for bundle in bundles]
        numDependencies = [bundle.numberOfDependencies for bundle in bundles]
        numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
        for bundle in bundles:
            ignored = any(ignoredSegment in bundle.path for ignoredSegment in ignoredPathSegments)
            if not ignored:
                nodeSize = self.interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
                self.addNode(bundle.name, width=str(nodeSize), height=str(nodeSize))
                for reqBundle in bundle.requiredBundles:
                    ignored = any(ignoredSegment in reqBundle for ignoredSegment in ignoredPathSegments)
                    if not ignored:
                        if reqBundle in bundleNames: 
                            nodeSize = self.interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                            self.addNode(reqBundle, width=str(nodeSize), height=str(nodeSize))
                        elif self.addNode(reqBundle, color=self.white): 
                            print ("Bundle %s is not contained in workspace." % reqBundle)
                        self.graph.add_edge(self.idForNames[bundle.name], self.idForNames[reqBundle], label="requires")
                for importedPackage in bundle.importedPackages:
                    self.addEdgeForPackageImport(bundle.name, importedPackage, bundlesForExports, numDependenciesForBundle)

    def interpolateLinear(self, numDependencies, maxNumDependencies):
        divisor = maxNumDependencies if maxNumDependencies > 0 else 1
        result = (numDependencies / divisor) * (self.maxNodeSize - self.minNodeSize) + self.minNodeSize
        return round(result,0)

    def addEdgeForPackageImport(self, sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in ignoredPathSegments)
            if not ignored: 
                nodeSize = self.interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
                self.addNode(exportingBundle.name, width=str(nodeSize), height=str(nodeSize))
                self.graph.add_edge(self.idForNames[sourceBundle], self.idForNames[exportingBundle.name], label="imports "+importedPackage)
        else:
            ignored = any(ignoredSegment in importedPackage for ignoredSegment in ignoredPathSegments)
            if not ignored: 
                if self.addNode(importedPackage, color=self.white, shape="rectangle"):
                    print ("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
                self.graph.add_edge(self.idForNames[sourceBundle], self.idForNames[importedPackage], label="imports")

    def addNode(self, bundleName, shape="ellipse", width="50", height="50", color=green):
        if bundleName not in self.idForNames:
            self.idForNames[bundleName] = str(self.nodeId)
            self.namesForId[self.nodeId] = bundleName
            self.graph.add_node(str(self.nodeId), label=bundleName, shape=shape, width=width, height=height, shape_fill=color)
            self.nodeId += 1
            return True
        return False

    def findCyclesRecursive(self, node, low, disc, stackMember, stack, cycles):
        disc[node] = self.time
        low[node] = self.time
        self.time += 1
        stackMember[node] = True
        stack.append(node)
        adjacentNodes = list([int(edge.node2) for edge in self.graph.edges.values() if int(edge.node1) == node])
        for adjacent in adjacentNodes:
            if disc[adjacent] == -1 :
                self.findCyclesRecursive(adjacent, low, disc, stackMember, stack, cycles)
                low[node] = min(low[node], low[adjacent])
            elif stackMember[adjacent] == True: 
                low[node] = min(low[node], disc[adjacent])
        # head node found, pop the stack and add SSC
        w = -1
        if low[node] == disc[node]:
            cycle = []
            while w != node:
                w = stack.pop()
                cycle.append(w)
                stackMember[w] = False
            cycles.append(cycle)

    #The function to do DFS traversal. 
    def getCycles(self):
        numNodes = len(self.graph.nodes)
        disc = [-1] * (numNodes)
        low = [-1] * (numNodes)
        stackMember = [False] * (numNodes)
        st =[]
        cycles = []
        for node in range(0,numNodes):
            if disc[node] == -1:
                cycles.append(self.findCyclesRecursive(node, low, disc, stackMember, st, cycles))
        return [cycle for cycle in cycles if None != cycle and len(cycle) > 1]

    def markCycles(self, cycles):
        for cycle in cycles:
            for nodeId in cycle:
                node = self.graph.nodes[str(nodeId)]
                setattr(node, "shape_fill", self.red)
                for edge in self.graph.edges.values():
                    fromNode = int(getattr(edge, "node1"))
                    toNode = int(getattr(edge, "node2"))
                    if fromNode in cycle and toNode in cycle:
                        setattr(edge, "color", self.red)

    def getNodes(self): return self.graph.nodes

    def getEdges(self): return self.graph.edges

    def serialize(self): return self.graph.get_graph()

class BundleParser:

    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignoredPathSegments = ignoredPathSegments

    def parseBundles(self):
        bundlePaths = self.scanForBundles()
        bundles = [self.parseBundle(bundle) for bundle in bundlePaths]
        return bundles

    def scanForBundles(self):
        bundels = set()
        for dirpath, dirNames, files in os.walk(self.directory):
            ignored = any(ignoredSegment in dirpath for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                for file in files:
                    if file == "MANIFEST.MF": 
                        bundels.add(os.path.dirname(dirpath))
        return bundels

    def parseBundle(self,bundlePath):
        manifestPath = bundlePath + "/META-INF/MANIFEST.MF"
        symbolicName, version, exportedPackages, importedPackages, requiredBundles = self.parseManifest(manifestPath)
        numberOfDependencies = len(requiredBundles)+len(importedPackages)
        bundle = Bundle(bundlePath, symbolicName, version, exportedPackages, importedPackages, requiredBundles, numberOfDependencies)
        return bundle

    def parseManifest(self,manifestPath):
        manifestContent = open(manifestPath, 'rb').read().decode()
        entries = re.split(r'[\r\n]+(?!\s)',manifestContent)
        requiredBundles = []
        importedPackages = []
        exportedPackages = []
        version = ""
        symbolicName = ""
        for entry in entries: 
            if entry.startswith("Require-Bundle:"):
                requiredBundles = [self.trim(bundle) for bundle in self.splitEntries(entry,"Require-Bundle:")]
            elif entry.startswith("Import-Package:"):
                importedPackages = [self.trim(package) for package in self.splitEntries(entry,"Import-Package:")]
            elif entry.startswith("Export-Package:"):
                # removes 'uses' declaration
                if ';' in entry: entry = entry[:entry.index(';')]
                exportedPackages = [self.trim(package) for package in self.splitEntries(entry,"Export-Package:")]
            elif entry.startswith("Bundle-Version:"):
                version = self.trim(entry.replace("Bundle-Version:", ""))
            elif entry.startswith("Bundle-SymbolicName:"):
                symbolicName = self.trim(entry.replace("Bundle-SymbolicName:", ""))
                if ";" in symbolicName:
                    symbolicName = symbolicName[:symbolicName.index(";")]
        # remove additional information
        requiredBundles[:] = [requiredBundle[:requiredBundle.index(";")]  if ";" in requiredBundle else requiredBundle for requiredBundle in requiredBundles]
        return symbolicName, version, exportedPackages, importedPackages, requiredBundles

    def trim(self, str):
        return str.replace("\n","").replace("\r","").strip(" ")

    def splitEntries(self, entry, entryName):
        return re.split(r",(?!\d)", entry.replace(entryName, ""))

    def mapBundlesOnExports(self, bundles):
        bundlesForExports = {}
        for bundle in bundles:
            for export in bundle.exportedPackages:
                bundlesForExports[export] = bundle
        return bundlesForExports

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
        return " ".join([self.name, self.version])

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
    bundleParser = BundleParser(workingDir, ignoredPathSegments)
    bundles = bundleParser.parseBundles()
    bundlesForExports = bundleParser.mapBundlesOnExports(bundles)
    print("Found %d bundle(s)"%len(bundles))
    print("Creating dependency graph...")
    graph = BundleGraph(bundles, bundlesForExports)
    print("Created dependency graph containing %d node(s) and %d edge(s)" % (len(graph.getNodes()), len(graph.getEdges())))
    print("Searching for cycles...")
    cycles = graph.getCycles()
    graph.markCycles(cycles)
    print("Found %d cycle(s)" % len(cycles))
    print("Writing output to %s" % str(workingDir))
    writeCyclesToTxt(os.path.join(workingDir,"bundle_cycles.txt"), cycles, graph)
    writeBundlesToCsv(os.path.join(workingDir,"bundles.csv"), bundles)
    writeGraphToGraphMl(os.path.join(workingDir,"dependencies.graphml"), graph)
