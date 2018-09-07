#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundle import Bundle
import pyyed

class BundleGraph:
    
    graph = pyyed.Graph() 
    nodeId = 0
    time = 0
    WHITE = "#FFFFFF"
    RED = "#FF0000"
    GREEN = "#00DB43"
    minNodeSize = 50
    maxNodeSize = 200
    idForNames = dict()
    namesForId = dict()
    
    def __init__(self, bundles, bundlesForExports, ignoredPathSegments):
        self.bundles = bundles
        self.bundlesForExports = bundlesForExports
        self.ignoredPathSegments = ignoredPathSegments
        self.__createDependencyGraph()
        
    def __createDependencyGraph(self):
        bundleNames = [bundle.name for bundle in self.bundles]
        numDependencies = [bundle.numberOfDependencies for bundle in self.bundles]
        numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
        for bundle in self.bundles:
            ignored = any(ignoredSegment in bundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored:
                nodeSize = self.__interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
                self.__addNode(bundle.name, width=str(nodeSize), height=str(nodeSize))
                for reqBundle in bundle.requiredBundles:
                    ignored = any(ignoredSegment in reqBundle for ignoredSegment in self.ignoredPathSegments)
                    if not ignored:
                        if reqBundle in bundleNames: 
                            nodeSize = self.__interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                            self.__addNode(reqBundle, width=str(nodeSize), height=str(nodeSize))
                        elif self.__addNode(reqBundle, color=self.WHITE): 
                            print ("Bundle %s is not contained in workspace." % reqBundle)
                        self.graph.add_edge(self.idForNames[bundle.name], self.idForNames[reqBundle], label="requires")
                for importedPackage in bundle.importedPackages:
                    self.__addEdgeForPackageImport(bundle.name, importedPackage, self.bundlesForExports, numDependenciesForBundle)

    def __interpolateLinear(self, numDependencies, maxNumDependencies):
        divisor = maxNumDependencies if maxNumDependencies > 0 else 1
        result = (numDependencies / divisor) * (self.maxNodeSize - self.minNodeSize) + self.minNodeSize
        return round(result,0)

    def __addEdgeForPackageImport(self, sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                nodeSize = self.__interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
                self.__addNode(exportingBundle.name, width=str(nodeSize), height=str(nodeSize))
                self.graph.add_edge(self.idForNames[sourceBundle], self.idForNames[exportingBundle.name], label="imports "+importedPackage)
        else:
            ignored = any(ignoredSegment in importedPackage for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                if self.__addNode(importedPackage, color=self.WHITE, shape="rectangle"):
                    print ("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
                self.graph.add_edge(self.idForNames[sourceBundle], self.idForNames[importedPackage], label="imports")

    def __addNode(self, bundleName, shape="ellipse", width="50", height="50", color=GREEN):
        if bundleName not in self.idForNames:
            self.idForNames[bundleName] = str(self.nodeId)
            self.namesForId[self.nodeId] = bundleName
            self.graph.add_node(str(self.nodeId), label=bundleName, shape=shape, width=width, height=height, shape_fill=color)
            self.nodeId += 1
            return True
        return False

    def __findCyclesRecursive(self, node, low, disc, stackMember, stack, cycles):
        disc[node] = self.time
        low[node] = self.time
        self.time += 1
        stackMember[node] = True
        stack.append(node)
        adjacentNodes = list([int(edge.node2) for edge in self.graph.edges.values() if int(edge.node1) == node])
        for adjacent in adjacentNodes:
            if disc[adjacent] == -1 :
                self.__findCyclesRecursive(adjacent, low, disc, stackMember, stack, cycles)
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
                cycles.append(self.__findCyclesRecursive(node, low, disc, stackMember, st, cycles))
        return [cycle for cycle in cycles if None != cycle and len(cycle) > 1]

    def markCycles(self, cycles):
        for cycle in cycles:
            for nodeId in cycle:
                node = self.graph.nodes[str(nodeId)]
                setattr(node, "shape_fill", self.RED)
                for edge in self.graph.edges.values():
                    fromNode = int(getattr(edge, "node1"))
                    toNode = int(getattr(edge, "node2"))
                    if fromNode in cycle and toNode in cycle:
                        setattr(edge, "color", self.RED)

    def getNodes(self): return self.graph.nodes

    def getEdges(self): return self.graph.edges

    def serialize(self): return self.graph.get_graph()