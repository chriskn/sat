#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sat.deps.graph.graph import Graph


class CycleTest(unittest.TestCase):
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

    def test_cycles_returns_empty_list_for_empty_graph(self):
        sut = Graph()
        sut.add_group("g1")

        cycles = sut.cycles()

        self.assertTrue(len(cycles) == 0)

    def test_cycles_returns_empty_list_for_empty_grouped_graph(self):
        sut = Graph()

        cycles = sut.cycles(grouped=True)

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

    def test_cycles_are_supported_for_numerical_and_string_ids(self):
        sut = Graph()
        sut.add_node("alpha")
        sut.add_node(2)
        sut.add_node(3)
        sut.add_node("4")
        sut.add_node("5")
        # cycle 1
        sut.add_edge("alpha", 2)
        sut.add_edge(2, 3)
        sut.add_edge(3, "alpha")

        sut.add_edge("4", "alpha")

        cycles = sut.cycles()

        self.assertEqual(cycles[0], [3, 2, "alpha"])
