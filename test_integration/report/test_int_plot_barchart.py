import os
import unittest
import shutil
import pytest

import pandas as pd

import sat.report.plot as sut
import test_integration.report.report_test_utils as reporttest


class PlotBarchartTest(unittest.TestCase):
    def setUp(self):
        self._ref_barchart_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_barchart.png"
        )
        self._ref_barchart_small_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_barchart_small.png"
        )
        self._used_file_name = "test_barchart.png"
        self._barchart_output_path = os.path.join(
            reporttest.TEST_RESULTS_FOLDER, self._used_file_name
        )

    @pytest.mark.integration
    def test_plot_barchart_plots_expected_barchart_if_dataframe_extends_max_limit(self):
        """Make shure barcharts are limit to _MAX_BARCHART_ENTRIES"""
        dummy_dataframe = pd.DataFrame(
            data=[
                ["Label %d" % dummyval, dummyval] for dummyval in list(range(-10, 100))
            ],
            columns=["Label", "Value"],
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
