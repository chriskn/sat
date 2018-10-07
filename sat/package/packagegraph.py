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

    def get_cycle_graph(self, cycles):
        graph = PackageGraph()
        for cycle in cycles:
            for node_label in cycle:
                node_id = self._id_for_name[node_label]
                node = self._graph.nodes[node_id]
                graph.add_node(node.label, shape=node.shape,
                               width=node.geom["width"], height=node.geom["height"], color=node.shape_fill)
            for edge in self._graph.edges.values():
                from_node = getattr(edge, "node1")
                to_node = getattr(edge, "node2")
                from_node_label = self._name_for_id[from_node]
                to_node_label = self._name_for_id[to_node]
                edge_label = getattr(edge, "label")
                if from_node_label in cycle and to_node_label in cycle:
                    graph.add_edge(from_node_label, to_node_label, edge_label)
        return graph
