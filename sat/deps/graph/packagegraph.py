#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

from sat.deps.graph.graph import Graph

_LOGGER = logging.getLogger(__name__)


class PackageGraph(Graph):

    _CLASS_IMPORT_PATTERN = re.compile(r".*\.[A-Z].*")

    def __init__(self, packages):
        Graph.__init__(self)
        _packages = packages
        self._add_packages(packages)
        self._add_dependencies(packages)

    def _add_dependencies(self, packages):
        for package in packages:
            for imp in package.imports():
                import_name = imp
                if self._CLASS_IMPORT_PATTERN.match(import_name):
                    import_name = re.split(r"\.[A-Z]", imp, maxsplit=1)[0]
                if import_name in self._id_for_name:
                    self.add_edge(package.name, import_name, "imports")

    def _add_packages(self, packages):
        num_deps = [len(p.imports()) for p in packages]
        max_num_deps = max(num_deps) if num_deps else 1
        for package in packages:
            node_size = self.interpolate_node_size(len(package.imports()), max_num_deps)
            self.add_node(package.name, width=node_size, height=node_size)

    def cycle_graph(self, cycles):
        graph = PackageGraph([])
        Graph.create_cycle_graph(graph, self, cycles)
        return graph
