import unittest

from sat.deps.graph.graph import Graph


class MarkCyclesTest(unittest.TestCase):
    def setUp(self):
        self._exp_color_cycle = "#FF0000"  # red
        self._exp_color_non_cycle_edge = "#000000"  # black
        self._exp_color_non_cycle_node = "#00DB43"  # green

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

        sut.mark_cycles(sut.cycles())
        node_colors = [node.shape_fill for node in sut.nodes().values()]

        self.assertEqual(
            node_colors,
            [
                self._exp_color_cycle,
                self._exp_color_cycle,
                self._exp_color_cycle,
                self._exp_color_non_cycle_node,
                self._exp_color_non_cycle_node,
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

        sut.mark_cycles(sut.cycles())
        edge_colors = [node.color for node in sut.edges().values()]

        self.assertEqual(
            edge_colors,
            [
                self._exp_color_cycle,
                self._exp_color_cycle,
                self._exp_color_cycle,
                self._exp_color_non_cycle_edge,
            ],
        )
