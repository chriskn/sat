#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=protected-access


def create(new_graph, old_graph, cycles, grouped=False):
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
