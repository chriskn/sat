# pylint: disable=R0201
# unused import

import sat.report.iplot as sut
import unittest


class TestInteractivePlot(unittest.TestCase):
    def test_heatmap(self):
        dummy_values = list(range(0, 5))
        data = [
            [0, 1, 9, 3, 2],
            [1, 2, 0, 2, 5],
            [0, 2, 3, 0, 5],
            [1, 2, 6, 4, 5],
            [1, 1, 3, 4, 5],
        ]
        x_labels = ["Index %d" % dummy_val for dummy_val in dummy_values]
        y_labels = ["Column %d" % dummy_val for dummy_val in dummy_values]
        sut.heatmap(x_labels, y_labels, data)

    def test_heatmap_much_data_long_labels(self):
        dummy_values = list(range(0, 50))
        data = [[dummyval] * len(dummy_values) for dummyval in dummy_values]
        x_labels = [
            "This is a very long index name for a heatmap %d" % dummy_val
            for dummy_val in dummy_values
        ]
        y_labels = [
            "This is a very long column name for a heatmap %d" % dummy_val
            for dummy_val in dummy_values
        ]
        sut.heatmap(x_labels, y_labels, data)

    def test_stacked_barchart(self):
        sut.stacked_barchart()

    def test_barchart(self):
        sut.barchart()
