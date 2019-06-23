#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyyed
from sat.deps.graph import tarjan


# pylint: disable=W0212,R0913,R0914,R1710
class Graph:

    _GREEN = "#00DB43"
    _RED = "#FF0000"
    _MIN_NODE_SIZE = 50
    _MAX_NODE_SIZE = 200

    @staticmethod
    def create_cycle_graph(new_graph, old_graph, cycles, grouped=False):
        for cycle in cycles:
            for node_label in cycle:
                node_id = old_graph._id_for_name[node_label]
                node = None
                if grouped:
                    node = old_graph._get_grouped_node(node_id)
                else:
                    node = old_graph.nodes()[node_id]
                new_graph.add_node(
                    node.label,
                    shape=node.shape,
                    width=node.geom["width"],
                    height=node.geom["height"],
                    shape_fill=node.shape_fill,
                )
            for edge in old_graph.edges().values():
                from_node = getattr(edge, "node1")
                to_node = getattr(edge, "node2")
                from_node_label = old_graph._name_for_id[int(from_node)]
                to_node_label = old_graph._name_for_id[int(to_node)]
                label = getattr(edge, "label")
                if from_node_label in cycle and to_node_label in cycle:
                    if grouped:
                        new_graph.add_edge(
                            from_node_label.split(".")[-1],
                            to_node_label.split(".")[-1],
                            label,
                        )
                    else:
                        new_graph.add_edge(from_node_label, to_node_label, label)
        return new_graph

    def __init__(self):
        self._graph = pyyed.Graph()
        self._node_id = 0
        self._id_for_name = dict()
        self._name_for_id = dict()

    def add_node(
        self,
        label,
        package_group=None,
        shape="rectangle",
        width="50",
        height="50",
        shape_fill=_GREEN,
        node_type="ShapeNode",
        uml=False,
    ):
        if label not in self._id_for_name:
            if package_group:
                fqn = package_group.label + "." + label
                package_group.add_node(
                    self._node_id,
                    label=label,
                    shape=shape,
                    width=width,
                    height=height,
                    shape_fill=shape_fill,
                    node_type=node_type,
                    UML=uml,
                )
                self._id_for_name[fqn] = self._node_id
                self._name_for_id[self._node_id] = fqn
            else:
                self._graph.add_node(
                    self._node_id,
                    label=label,
                    shape=shape,
                    width=width,
                    height=height,
                    shape_fill=shape_fill,
                    node_type=node_type,
                    UML=uml,
                )
                self._id_for_name[label] = self._node_id
                self._name_for_id[self._node_id] = label
            self._node_id += 1
            return True
        return False

    def add_edge(
        self, source, target, label="", line_type="line", arrowhead="standard"
    ):
        source_id = self._id_for_name[source]
        target_id = self._id_for_name[target]
        self._graph.add_edge(
            source_id, target_id, label=label, line_type=line_type, arrowhead=arrowhead
        )

    def add_group(self, label, shape="rectangle", fill="#ffd35b"):
        self._id_for_name[label] = self._node_id
        self._name_for_id[self._node_id] = label
        group = self._graph.add_group(
            str(self._node_id), label=label, shape=shape, fill=fill
        )
        self._node_id += 1
        return group

    def cycles(self, grouped=False):
        cycles = tarjan.scns(self._graph, grouped)
        named_cycles = []
        for cycle in cycles:
            named_cycles.append([self._name_for_id[_id] for _id in cycle])
        return named_cycles

    def mark_cycles(self, cycles, grouped=False):
        for cycle in cycles:
            for node_label in cycle:
                node_id = self._id_for_name[node_label]
                node = None
                if grouped:
                    node = self._get_grouped_node(node_id)
                else:
                    node = self._graph.nodes[node_id]
                setattr(node, "shape_fill", self._RED)
                for edge in self._graph.edges.values():
                    from_node = self._name_for_id[getattr(edge, "node1")]
                    to_node = self._name_for_id[getattr(edge, "node2")]
                    if from_node in cycle and to_node in cycle:
                        setattr(edge, "color", self._RED)

    def _get_grouped_node(self, node_id):
        for group in self._graph.groups.values():
            if node_id in group.nodes:
                return group.nodes[node_id]

    def nodes(self):
        return self._graph.nodes

    def edges(self):
        return self._graph.edges

    def serialize(self):
        return self._graph.get_graph()

    def interpolate_node_size(self, num_deps, max_num_deps):
        divisor = max_num_deps if max_num_deps > 0 else 1
        result = (num_deps / divisor) * (
            self._MAX_NODE_SIZE - self._MIN_NODE_SIZE
        ) + self._MIN_NODE_SIZE
        return str(round(result, 0))
