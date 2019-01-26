#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

from deps.graph.graph import Graph

logger = logging.getLogger(__name__)


class PackageGraph(Graph):

    _CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')

    def __init__(self, packages=[]):
        Graph.__init__(self)
        _packages = packages
        numdeps = [len(p.imports()) for p in packages]
        max_numdeps = max(numdeps) if len(numdeps) > 0 else 1
        for package in packages:
            node_size = self.interpolate_node_size(
                len(package.imports()), max_numdeps)
            self.add_node(package.name, width=node_size, height=node_size)
        for package in packages:
            for imp in package.imports():
                import_name = imp
                if self._CLASS_IMPORT_PATTERN.match(import_name):
                    import_name = re.split(r'\.[A-Z]', imp, maxsplit=1)[0]
                if import_name in self._id_for_name:
                    self.add_edge(package.name, import_name, "imports")

    def cycle_graph(self, cycles):
        graph = PackageGraph()
        Graph.cycle_graph(graph, self, cycles)
        return graph
