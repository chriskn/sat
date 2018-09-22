#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph
from domain import Package

class PackageGraph(Graph):

    _packages = None

    def __init__(self, packages=[]):
        Graph.__init__(self)
        self._packages = packages
        for package in packages:
            self.addNode(package.name)
            for imp in package.getImports():
                if not self.containsNode(imp):
                    self.addNode(imp)
                self.addEdge(package.name, imp, "imports")
    
    def getCycleGraph(self, cycles):
        graph = PackageGraph()
        for cycle in cycles:
            for nodeLabel in cycle:
                nodeId = self._idForNames[nodeLabel]
                node = self._graph.nodes[nodeId]
                graph.addNode(node.label, shape=node.shape, width=node.geom["width"], height=node.geom["height"], color=node.shape_fill) 
            for edge in self._graph.edges.values():
                fromNode = getattr(edge, "node1")
                toNode = getattr(edge, "node2")
                fromNodeLabel = self._namesForId[int(fromNode)]
                toNodeLabel = self._namesForId[int(toNode)]
                label =  getattr(edge, "label")
                if fromNodeLabel in cycle and toNodeLabel in cycle:
                    graph.addEdge(fromNodeLabel, toNodeLabel, label)
        return graph
