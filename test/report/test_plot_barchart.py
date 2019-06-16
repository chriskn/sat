import os
import unittest
import shutil
import mock
import pytest

import pandas as pd

import sat.report.plot as sut
import test.report.report_test_utils as reporttest


class PlotBarchartTest(unittest.TestCase):
    def setUp(self):
        self._ref_barchart_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_barchart.png"
        )
        self._used_file_name = "test_barchart.png"
        self._barchart_output_path = os.path.join(
            reporttest.TEST_RESULTS_FOLDER, self._used_file_name
        )

    @mock.patch("sat.report.plot._write_figure")
    def test_plot_barchart_does_not_plot_if_dataframe_empty(self, mock_writer):
        sut.plot_barchart(pd.DataFrame(), "", "", "", "")

        self.assertFalse(mock_writer.called)

    def test_plot_treemap_logs_exp_message_for_empty_dataframe(self):
        used_file_name = "dummyFileName"
        exp_logger_name = sut.__name__

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_barchart(pd.DataFrame(), "dummyTitle", "", "", used_file_name)

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":No data available. Skip writing barchart: "
                    + used_file_name
                ],
            )

    @pytest.mark.integration
    def test_plot_barchart_plots_expected_barchart_if_dataframe_extends_max_limit(self):
        """Make shure barcharts are limit to _MAX_BARCHART_ENTRIES"""
        dummy_dataframe = pd.DataFrame(
            data=[
                ["Label %d" % dummyval, dummyval] for dummyval in list(range(-10, 100))
            ]
        )
        sut.plot_barchart(
            dummy_dataframe,
            "bla",
            "dummyTitle",
            reporttest.TEST_RESULTS_FOLDER,
            self._used_file_name,
        )

        reporttest.assert_images_equal(
            self._barchart_output_path, self._ref_barchart_path
        )

    def tearDown(self):
        shutil.rmtree(reporttest.TEST_RESULTS_FOLDER, ignore_errors=True)
