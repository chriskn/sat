import unittest

import mock
import pandas as pd

import sat.report.plot as sut


class PlotHeatmapTest(unittest.TestCase):
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
