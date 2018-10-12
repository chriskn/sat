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
            self.add_node(package.name)
            for imp in package.imports():
                if not self.contains_node(imp):
                    self.add_node(imp)
                self.add_edge(package.name, imp, "imports")

    def cycle_graph(self, cycles):
        graph = PackageGraph()
        Graph.cycle_graph(graph, self , cycles)
        return graph