import unittest
import mock

import pandas as pd

import sat.report.plot as sut


class PlotBarchartTest(unittest.TestCase):
    @mock.patch("sat.report.plot._write_figure_and_reset")
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
