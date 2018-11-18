#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph
import re, logging

logger = logging.getLogger(__name__)

class PackageGraph(Graph):

    _CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')

    def __init__(self, packages=[]):
        Graph.__init__(self)
        _packages = packages
        for package in packages:
            self.add_node(package.name)    
        for package in packages:
            for imp in package.imports():
                import_name = imp
                #import_path = re.split(":", imp)[0]
                if self._CLASS_IMPORT_PATTERN.match(import_name):
                    import_name = re.split(r'\.[A-Z]', imp, maxsplit=1)[0]
                if import_name in self._id_for_name:
                    self.add_edge(package.name, import_name, "imports")

    def cycle_graph(self, cycles):
        graph = PackageGraph()
        Graph.cycle_graph(graph, self , cycles)
        return graph