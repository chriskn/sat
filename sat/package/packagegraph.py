#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph
from domain import Package
import re


class PackageGraph(Graph):


    def __init__(self, packages=[]):
        Graph.__init__(self)
        _packages = packages
        _CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')
        for package in packages:
            self.add_node(package.name)
            for imp in package.imports():
                package_imp = imp
                if _CLASS_IMPORT_PATTERN.match(imp):
                    package_imp = re.split(r'\.[A-Z]', imp, maxsplit=1)[0]
                if not self.contains_node(package_imp):
                    self.add_node(package_imp)
                self.add_edge(package.name, package_imp, "imports")

    def cycle_graph(self, cycles):
        graph = PackageGraph()
        Graph.cycle_graph(graph, self , cycles)
        return graph