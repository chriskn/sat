#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundle import Bundle
import pyyed

class BundleGraph:

    _WHITE = "#FFFFFF"
    _RED = "#FF0000"
    _GREEN = "#00DB43"
    _MIN_NODE_SIZE = 50
    _MAX_NODE_SIZE = 200

    _graph = pyyed.Graph() 
    _nodeId = 0
    _time = 0
    _idForNames = dict()
    _namesForId = dict()
    
    def __init__(self, bundles, bundlesForExports, ignoredPathSegments):
        self.bundles = bundles
        self.bundlesForExports = bundlesForExports
        self.ignoredPathSegments = ignoredPathSegments
        self._createDependencyGraph()
        
    def _createDependencyGraph(self):
        bundleNames = [bundle.name for bundle in self.bundles]
        numDependencies = [bundle.numberOfDependencies for bundle in self.bundles]
        numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
        for bundle in self.bundles:
            ignored = any(ignoredSegment in bundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored:
                nodeSize = self._interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
                self._addNode(bundle.name, width=str(nodeSize), height=str(nodeSize))
                for reqBundle in bundle.requiredBundles:
                    ignored = any(ignoredSegment in reqBundle for ignoredSegment in self.ignoredPathSegments)
                    if not ignored:
                        if reqBundle in bundleNames: 
                            nodeSize = self._interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                            self._addNode(reqBundle, width=str(nodeSize), height=str(nodeSize))
                        elif self._addNode(reqBundle, color=self._WHITE): 
                            print ("Bundle %s is not contained in workspace." % reqBundle)
                        self._graph.add_edge(self._idForNames[bundle.name], self._idForNames[reqBundle], label="requires")
                for importedPackage in bundle.importedPackages:
                    self._addEdgeForPackageImport(bundle.name, importedPackage, self.bundlesForExports, numDependenciesForBundle)

    def _interpolateLinear(self, numDependencies, maxNumDependencies):
        divisor = maxNumDependencies if maxNumDependencies > 0 else 1
        result = (numDependencies / divisor) * (self._MAX_NODE_SIZE - self._MIN_NODE_SIZE) + self._MIN_NODE_SIZE
        return round(result,0)

    def _addEdgeForPackageImport(self, sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                nodeSize = self._interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
                self._addNode(exportingBundle.name, width=str(nodeSize), height=str(nodeSize))
                self._graph.add_edge(self._idForNames[sourceBundle], self._idForNames[exportingBundle.name], label="imports "+importedPackage)
        else:
            ignored = any(ignoredSegment in importedPackage for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                if self._addNode(importedPackage, color=self._WHITE, shape="rectangle"):
                    print ("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
                self._graph.add_edge(self._idForNames[sourceBundle], self._idForNames[importedPackage], label="imports")

    def _addNode(self, bundleName, shape="ellipse", width="50", height="50", color=_GREEN):
        if bundleName not in self._idForNames:
            self._idForNames[bundleName] = str(self._nodeId)
            self._namesForId[self._nodeId] = bundleName
            self._graph.add_node(str(self._nodeId), label=bundleName, shape=shape, width=width, height=height, shape_fill=color)
            self._nodeId += 1
            return True
        return False

    def _findCyclesRecursive(self, node, low, disc, stackMember, stack, cycles):
        disc[node] = self._time
        low[node] = self._time
        self._time += 1
        stackMember[node] = True
        stack.append(node)
        adjacentNodes = list([int(edge.node2) for edge in self._graph.edges.values() if int(edge.node1) == node])
        for adjacent in adjacentNodes:
            if disc[adjacent] == -1 :
                self._findCyclesRecursive(adjacent, low, disc, stackMember, stack, cycles)
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
        numNodes = len(self._graph.nodes)
        disc = [-1] * (numNodes)
        low = [-1] * (numNodes)
        stackMember = [False] * (numNodes)
        st =[]
        cycles = []
        for node in range(0,numNodes):
            if disc[node] == -1:
                cycles.append(self._findCyclesRecursive(node, low, disc, stackMember, st, cycles))
        return [cycle for cycle in cycles if None != cycle and len(cycle) > 1]

    def markCycles(self, cycles):
        for cycle in cycles:
            for nodeId in cycle:
                node = self._graph.nodes[str(nodeId)]
                setattr(node, "shape_fill", self._RED)
                for edge in self._graph.edges.values():
                    fromNode = int(getattr(edge, "node1"))
                    toNode = int(getattr(edge, "node2"))
                    if fromNode in cycle and toNode in cycle:
                        setattr(edge, "color", self._RED)

    def getNodes(self): return self._graph.nodes

    def getEdges(self): return self._graph.edges

    def serialize(self): return self._graph.get_graph()