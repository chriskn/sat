#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import shutil
import pytest

import pandas as pd

import sat.report.plot as sut
import test_integration.report.report_test_utils as reporttest


class PlotHeatmapIntTest(unittest.TestCase):
    def setUp(self):
        self._ref_heatmap_path = os.path.join(
            reporttest.REF_DATA_FOLDER, "ref_heatmap.png"
        )
        self._used_file_name = "test_heatmap.png"
        self._heatmap_output_path = os.path.join(
            reporttest.TEST_RESULTS_FOLDER, self._used_file_name
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
