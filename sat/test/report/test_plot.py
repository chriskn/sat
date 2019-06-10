import unittest
import report.plot as sut
import os
import pandas as pd

_COLUMNS = [
    "GROUP",
    "PACKAGE",
    "CLASS",
    "INSTRUCTION_MISSED",
    "INSTRUCTION_COVERED",
    "BRANCH_MISSED",
    "BRANCH_COVERED",
    "LINE_MISSED",
    "LINE_COVERED",
    "COMPLEXITY_MISSED",
    "COMPLEXITY_COVERED",
    "METHOD_MISSED",
    "METHOD_COVERED",
]


class PlotTest(unittest.TestCase):
    def test_plot_scatterplot(self):
        # pylint: disable=R0201
        # work in progress
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_testdata = os.path.join(cur_dir, "testdata", "coverage.csv")
        data = pd.read_csv(path_to_testdata)
        columns_to_drop = list(_COLUMNS)
        columns_to_drop.remove(_COLUMNS[2])
        columns_to_drop.remove(_COLUMNS[3])
        columns_to_drop.remove(_COLUMNS[4])
        columns_to_drop.remove(_COLUMNS[9])
        dropped = data.drop(columns=columns_to_drop)
        sut.plot_scatterplot(dropped, os.path.dirname(path_to_testdata), "test")
