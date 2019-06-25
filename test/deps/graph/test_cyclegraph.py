import unittest
from sat.deps.graph.graph import Graph
import sat.deps.graph.cyclegraph as sut


class CycleGraphTest(unittest.TestCase):
    def test_create_creates_expected_graph_for_simple_cycle(self):
        graph = Graph()
        graph.add_node("1")
        graph.add_node("2")
        graph.add_node("3")
        graph.add_node("4")
        # cycle 1
        graph.add_edge("1", "2")
        graph.add_edge("2", "3")
        graph.add_edge("3", "1")

        cycle_graph = sut.create(Graph(), graph, graph.cycles())
        nodes = cycle_graph.nodes().values()

        self.assertEqual([node.label for node in nodes], ["3", "2", "1"])

    def test_create_creates_empty_graph_for_graph_without_cycles(self):
        graph = Graph()
        graph.add_node("1")
        graph.add_node("2")
        graph.add_node("3")
        # cycle 1
        graph.add_edge("1", "2")
        graph.add_edge("2", "3")

        cycle_graph = sut.create(Graph(), graph, graph.cycles())
        nodes = cycle_graph.nodes()

        self.assertEqual(len(nodes), 0)

    def test_create_creates_empty_graph_for_empty_graph(self):
        empty_graph = Graph()

        cycle_graph = sut.create(Graph(), empty_graph, empty_graph.cycles())
        nodes = cycle_graph.nodes()

        self.assertEqual(len(nodes), 0)
