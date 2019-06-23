#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sat.deps.graph.graph import Graph


class GraphTest(unittest.TestCase):
    def test_cycles_returns_exp_for_one_cycle(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")
        sut.add_edge("3", "4")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 1)
        self.assertEqual(cycles, [["3", "2", "1"]])

    def test_cycles_returns_exp_for_two_cycles(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        sut.add_edge("1", "2")
        sut.add_edge("2", "1")
        sut.add_edge("3", "4")
        sut.add_edge("4", "3")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 2)
        self.assertEqual(cycles, [["2", "1"], ["4", "3"]])

    def test_cycles_returns_empty_list_for_no_cycles(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "4")
        sut.add_edge("4", "5")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 0)

    def test_cycles_returns_empty_list_for_empty_graph(self):
        sut = Graph()

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 0)

    def test_cycles_returns_exp_for_two_connected_cycles(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        sut.add_node("6")
        sut.add_node("7")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")
        # cycle 2
        sut.add_edge("4", "5")
        sut.add_edge("5", "6")
        sut.add_edge("6", "4")
        # connecting cycles
        sut.add_edge("6", "7")
        sut.add_edge("3", "7")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 2)
        self.assertEqual(cycles, [["3", "2", "1"], ["6", "5", "4"]])

    def test_cycles_returns_one_cycle_for_two_cyclic_connected_cycles(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        sut.add_node("6")
        sut.add_node("7")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")
        # cycle 2
        sut.add_edge("4", "5")
        sut.add_edge("5", "6")
        sut.add_edge("6", "4")
        # connecting cycles
        sut.add_edge("3", "4")
        sut.add_edge("4", "3")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 1)
        self.assertEqual(cycles, [["6", "5", "4", "3", "2", "1"]])

    def test_create_cycle_graph_creates_expected_graph_for_simple_cycle(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")

        cycle_graph = Graph.create_cycle_graph(Graph(), sut, sut.cycles())
        nodes = cycle_graph.nodes().values()

        self.assertEqual(len(nodes), 3)
        self.assertEqual([node.label for node in nodes], ["3", "2", "1"])

    def test_create_cycle_graph_creates_empty_graph_for_graph_without_cycles(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")

        cycle_graph = Graph.create_cycle_graph(Graph(), sut, sut.cycles())
        nodes = cycle_graph.nodes()

        self.assertEqual(len(nodes), 0)

    def test_create_cycle_graph_creates_empty_graph_for_empty_graph(self):
        sut = Graph()

        cycle_graph = Graph.create_cycle_graph(Graph(), sut, sut.cycles())
        nodes = cycle_graph.nodes()

        self.assertEqual(len(nodes), 0)

    def test_mark_cycle_marks_only_cyclic_nodes(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")

        sut.add_edge("4", "1")

        exp_color_cycle = "#FF0000"  # red
        exp_color_no_cycle = "#00DB43"  # green

        sut.mark_cycles(sut.cycles())
        node_colors = [node.shape_fill for node in sut.nodes().values()]

        self.assertEqual(
            node_colors,
            [
                exp_color_cycle,
                exp_color_cycle,
                exp_color_cycle,
                exp_color_no_cycle,
                exp_color_no_cycle,
            ],
        )

    def test_mark_cycle_marks_only_cyclic_edges(self):
        sut = Graph()
        sut.add_node("1")
        sut.add_node("2")
        sut.add_node("3")
        sut.add_node("4")
        sut.add_node("5")
        # cycle 1
        sut.add_edge("1", "2")
        sut.add_edge("2", "3")
        sut.add_edge("3", "1")

        sut.add_edge("4", "1")

        exp_color_cycle = "#FF0000"  # red
        exp_color_no_cycle = "#000000"  # black

        sut.mark_cycles(sut.cycles())
        edge_colors = [node.color for node in sut.edges().values()]

        self.assertEqual(
            edge_colors,
            [exp_color_cycle, exp_color_cycle, exp_color_cycle, exp_color_no_cycle],
        )
