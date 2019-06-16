import os
import unittest
import shutil
import mock
import pytest

import pandas as pd

import sat.report.plot as sut
import test.report.report_test_utils as reporttest

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


class PlotTreemapTest(unittest.TestCase):
    def setUp(self):
        self._cur_dir = os.path.dirname(os.path.abspath(__file__))
        self._ref_data_folder = os.path.join(self._cur_dir, "test_data")
        self._ref_treemap_path = os.path.join(self._ref_data_folder, "ref_treemap.png")
        self._ref_treemap_path_longlabels = os.path.join(
            self._ref_data_folder, "ref_treemap_long_labels.png"
        )
        self._test_results_folder = os.path.join(self._cur_dir, "test_results")
        self._used_file_name = "test_treemap.png"
        self._treemap_output_path = os.path.join(
            self._test_results_folder, self._used_file_name
        )

    # def test_plot_scatterplot(self):
    # pylint: disable=R0201
    # work in progress
    # used_coverage = os.path.join(self._cur_dir, "coverage.csv")

    # data = pd.read_csv(path_to_testdata)
    # columns_to_drop = list(_COLUMNS)
    # columns_to_drop.remove(_COLUMNS[2])
    # columns_to_drop.remove(_COLUMNS[3])
    # columns_to_drop.remove(_COLUMNS[4])
    # columns_to_drop.remove(_COLUMNS[9])
    # dropped = data.drop(columns=columns_to_drop)
    # sut.plot_scatterplot(dropped, os.path.dirname(path_to_testdata), "test")

    @mock.patch("sat.report.plot._write_figure")
    def test_plot_treemap_does_not_plot_if_dataframe_empty(self, mock_writer):
        sut.plot_treemap(pd.DataFrame(), "", "", "", "")

        self.assertFalse(mock_writer.called)

    @mock.patch("sat.report.plot._write_figure")
    def test_plot_treemap_does_not_plot_if_dataframe_contains_zero(self, mock_writer):
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val] for dummy_val in list(range(0, 22))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        sut.plot_treemap(dummy_dataframe, "", "", "", "")

        self.assertFalse(mock_writer.called)

    def test_plot_treemap_logs_exp_message_for_empty_dataframe(self):
        used_file_name = "dummyFileName"
        exp_logger_name = sut.__name__

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_treemap(pd.DataFrame(), "dummyTitle", "", used_file_name, "")

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":No data available. Skip writing treemap: "
                    + used_file_name
                ],
            )

    def test_plot_treemap_logs_exp_message_if_dataframe_contains_zero(self):
        used_file_name = "dummyFileName"
        exp_logger_name = sut.__name__
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val] for dummy_val in list(range(0, 20))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_treemap(dummy_dataframe, "", "", used_file_name, "")

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":Can't create treemap with 0 values. Skip writing treemap: "
                    + used_file_name
                ],
            )

    def test_plot_treemap_logs_exp_message_if_data_extends_max_limit(self):
        used_file_name = "test_treemap.png"
        exp_logger_name = sut.__name__
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val] for dummy_val in list(range(1, 22))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        with self.assertLogs(exp_logger_name, level="INFO") as mock_log:
            sut.plot_treemap(
                dummy_dataframe,
                "dummyTitle",
                self._test_results_folder,
                used_file_name,
                "",
            )

            self.assertEqual(
                mock_log.output,
                [
                    "INFO:"
                    + exp_logger_name
                    + ":Number of entries (21) exceeds limit for treemaps. Limiting entries to 20 for treemap: "
                    + used_file_name
                ],
            )

    @pytest.mark.integration
    def test_plot_treemap_plots_exp_treemap_if_data_extends_max_limit(self):
        dummy_data = [
            ["Entry name %s" % dummy_val, dummy_val] for dummy_val in list(range(1, 22))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        sut.plot_treemap(
            dummy_dataframe,
            "dummyTitle",
            self._test_results_folder,
            self._used_file_name,
            "value label",
        )

        reporttest.assert_images_equal(
            self._treemap_output_path, self._ref_treemap_path
        )

    @pytest.mark.integration
    def test_plot_treemap_wraps_long_labels(self):
        dummy_data = [
            ["Entry name with long long long label %s" % dummy_val, dummy_val]
            for dummy_val in list(range(1, 21))
        ]
        dummy_dataframe = pd.DataFrame(dummy_data)

        sut.plot_treemap(
            dummy_dataframe,
            "dummyTitle",
            self._test_results_folder,
            self._used_file_name,
            "",
        )

        reporttest.assert_images_equal(
            self._treemap_output_path, self._ref_treemap_path_longlabels
        )

    def tearDown(self):
        shutil.rmtree(self._test_results_folder, ignore_errors=True)
