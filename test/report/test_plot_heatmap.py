import os
import unittest
import shutil
import mock
import pytest

import pandas as pd

import sat.report.plot as sut
import test.report.report_test_utils as reporttest


class PlotHeatmapTest(unittest.TestCase):
    def setUp(self):
        self._ref_heatmap_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_heatmap.png"
        )
        self._used_file_name = "test_heatmap.png"
        self._heatmap_output_path = os.path.join(
            reporttest.TEST_RESULTS_FOLDER, self._used_file_name
        )

    @mock.patch("sat.report.plot._write_figure")
    def test_plot_heatmap_does_not_plot_if_dataframe_empty(self, mock_writer):
        sut.plot_heatmap(pd.DataFrame(), "", "", "")

        self.assertFalse(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure")
    def test_plot_heatmap_does_not_plot_if_dataframe_extends_max_limit(
        self, mock_writer
    ):
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val]
            for dummy_val in list(range(0, 201))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        sut.plot_heatmap(dummy_dataframe, "", "", "")

        self.assertFalse(mock_writer.called)

    def test_plot_heatmap_logs_exp_message_for_empty_dataframe(self):
        used_file_name = "dummyFileName"
        exp_logger_name = sut.__name__

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_heatmap(pd.DataFrame(), "dummyTitle", "", used_file_name)

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":No data available. Skip writing heatmap: "
                    + used_file_name
                ],
            )

    def test_plot_heatmap_logs_exp_message_if_dataframe_extends_max_limit(self):
        used_file_name = "dummyFileName"
        exp_logger_name = sut.__name__
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val]
            for dummy_val in list(range(0, 201))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_heatmap(dummy_dataframe, "dummyTitle", "", used_file_name)

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":Number of entries is 201 and exceeds limit of 200 for heatmaps. Will skip creation of heatmap: "
                    + used_file_name
                ],
            )

    @pytest.mark.integration
    def test_plot_heatmap_plots_exp_heatmap(self):
        dummy_values = list(range(0, 5))
        dummy_dataframe = pd.DataFrame(
            data=[
                [0, 1, 9, 3, 4],
                [1, 2, 3, 2, 5],
                [0, 2, 3, -4, 5],
                [1, 2, 6, 4, 5],
                [1, -1, 3, 4, 5],
            ],
            index=["Index %d" % dummy_val for dummy_val in dummy_values],
            columns=["Column %d" % dummy_val for dummy_val in dummy_values],
        )

        sut.plot_heatmap(
            dummy_dataframe,
            "dummyTitle",
            reporttest.TEST_RESULTS_FOLDER,
            self._used_file_name,
        )

        reporttest.assert_images_equal(
            self._heatmap_output_path, self._ref_heatmap_path
        )

    def tearDown(self):
        shutil.rmtree(reporttest.TEST_RESULTS_FOLDER, ignore_errors=True)
