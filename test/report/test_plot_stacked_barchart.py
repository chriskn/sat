#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock

import pandas as pd

import sat.report.plot as sut


class PlotStackedBarchartTest(unittest.TestCase):
    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_stacked_barchart_does_not_plot_if_dataframe_empty(self, mock_writer):
        sut.plot_stacked_barchart(pd.DataFrame(), "", "", "", "")

        self.assertFalse(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_stacked_barchart_does_plot(self, mock_writer):
        dummy_dataframe = pd.DataFrame(
            data=[
                ["Label %d" % dummyval, dummyval, dummyval]
                for dummyval in list(range(0, 10))
            ],
            columns=["Label", "Value 1", "Value 2"],
        )
        sut.plot_stacked_barchart(dummy_dataframe, "", "", "", "")

        self.assertTrue(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure_and_reset")
    def test_plot_stacked_barchart_does_plot_if_data_extends_max_limit(
        self, mock_writer
    ):
        dummy_dataframe = pd.DataFrame(
            data=[
                [
                    "Label with long long long long long long long long long long long long long long text %d"
                    % dummyval,
                    dummyval,
                    dummyval,
                ]
                for dummyval in list(range(0, 100))
            ],
            columns=["Label", "Value 1", "Value 2"],
        )
        sut.plot_stacked_barchart(dummy_dataframe, "", "", "", "")

        self.assertTrue(mock_writer.called)
