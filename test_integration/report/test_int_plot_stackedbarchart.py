import os
import unittest
import shutil
import pytest

import pandas as pd

import sat.report.plot as sut
import test_integration.report.report_test_utils as reporttest


class PlotStackedBarchartTest(unittest.TestCase):
    def setUp(self):
        self._ref_stacked_barchart_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_stacked_barchart.png"
        )
        self._used_file_name = "test_stacked_barchart.png"
        self._stacked_barchart_output_path = os.path.join(
            reporttest.TEST_RESULTS_FOLDER, self._used_file_name
        )

    @pytest.mark.integration
    def test_plot_stacked_barchart_plots_expected_barchart_if_dataframe_extends_max_limit(
        self
    ):
        """Make shure barcharts are limit to _MAX_BARCHART_ENTRIES"""
        dummy_dataframe = pd.DataFrame(
            data=[
                ["Label %d" % dummyval, dummyval, dummyval * 0.5]
                for dummyval in list(range(-10, 100))
            ],
            columns=["Labels", "Lines Added", "Lines Removed"],
        )
        sut.plot_stacked_barchart(
            dummy_dataframe,
            "total",
            "dummyTitle",
            reporttest.TEST_RESULTS_FOLDER,
            self._used_file_name,
        )

        reporttest.assert_images_equal(
            self._stacked_barchart_output_path, self._ref_stacked_barchart_path
        )

    def tearDown(self):
        shutil.rmtree(reporttest.TEST_RESULTS_FOLDER, ignore_errors=True)
