#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock

import pandas as pd

import sat.report.plot as sut


class PlotBarchartTest(unittest.TestCase):
    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_barchart_does_not_plot_if_dataframe_empty(self, mock_writer):
        sut.plot_barchart(pd.DataFrame(), "", "", "", "")

        self.assertFalse(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_barchart_does_plot(self, mock_writer):
        dummy_dataframe = pd.DataFrame(
            data=[["Label %d" % dummyval, dummyval] for dummyval in list(range(0, 10))],
            columns=["Label", "Value"],
        )
        sut.plot_barchart(dummy_dataframe, "", "", "", "")

        self.assertTrue(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_barchart_does_plot_if_data_extends_max_limit(self, mock_writer):
        dummy_dataframe = pd.DataFrame(
            data=[
                [
                    "Label with long long long long long long long long long long long long long long text %d"
                    % dummyval,
                    dummyval,
                ]
                for dummyval in list(range(0, 100))
            ],
            columns=["Label", "Value"],
        )
        sut.plot_barchart(dummy_dataframe, "", "", "", "")

        self.assertTrue(mock_writer.called)
