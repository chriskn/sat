#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import ANY

import mock
from pandas.util.testing import assert_frame_equal

from sat.changes.analyser.filechanges import FileChanges
from sat.changes.domain import Change

_PROJ_PATH_1 = os.path.join("my", "dummy", "proj1")
_PROJ_PATH_2 = os.path.join("my", "dummy", "proj2")
_PROJ_PATH_3 = os.path.join("my", "dummy", "proj3")


_REL_PACK_PATH_1 = os.path.join("a", "b")
_REL_PACK_PATH_1_2 = os.path.join("a", "b")  # split package
_REL_PACK_PATH_3 = os.path.join("c", "d")
_REL_PACK_PATH_4 = os.path.join("e", "f", "g")
_REL_PACK_PATH_5 = os.path.join("e", "f", "h")


_ABS_PACKAGE_PATH_1 = os.path.join(_PROJ_PATH_1, _REL_PACK_PATH_1)
_ABS_PACKAGE_PATH_1_2 = os.path.join(_PROJ_PATH_2, _REL_PACK_PATH_1_2)
_ABS_PACKAGE_PATH_3 = os.path.join(_PROJ_PATH_2, _REL_PACK_PATH_3)
_ABS_PACKAGE_PATH_4 = os.path.join(_PROJ_PATH_3, _REL_PACK_PATH_4)
_ABS_PACKAGE_PATH_5 = os.path.join(_PROJ_PATH_3, _REL_PACK_PATH_5)

_REL_PACK_PATH_FOR_PACK_PATH = {
    _ABS_PACKAGE_PATH_1: _REL_PACK_PATH_1,
    _ABS_PACKAGE_PATH_1_2: _REL_PACK_PATH_1_2,
    ".." + os.sep + _ABS_PACKAGE_PATH_3: _REL_PACK_PATH_3,
    os.sep + _ABS_PACKAGE_PATH_4: _REL_PACK_PATH_4,
    "." + os.sep + _ABS_PACKAGE_PATH_5: _REL_PACK_PATH_5,
}

_CHANGE_1 = "dummy1.java"
_CHANGE_2 = "dummy2.java"
_CHANGE_3 = "dummy3.java"
_CHANGE_4 = "dummy4.java"

_CHANGE_PATH_1 = os.path.join(_ABS_PACKAGE_PATH_1, _CHANGE_1)
_CHANGE_PATH_2 = os.path.join(_ABS_PACKAGE_PATH_1_2, _CHANGE_2)
_CHANGE_PATH_3 = os.path.join(_ABS_PACKAGE_PATH_3, _CHANGE_3)
_CHANGE_PATH_4 = os.path.join(_ABS_PACKAGE_PATH_4, _CHANGE_4)

_CHANGES = [
    Change(_CHANGE_PATH_1, 10, 20),
    Change(_CHANGE_PATH_2, 0, 20),
    Change(_CHANGE_PATH_3, 55, 20),
    Change(_CHANGE_PATH_4, 0, 0),
]


class FileChangesTest(unittest.TestCase):
    # allow protected-access
    # pylint: disable = W0212

    def setUp(self):
        self.expected_since = "12.10.2018"
        self.sut = FileChanges(self.expected_since)

    def test_name_is_files(self):
        self.assertEqual(FileChanges.name(), "files")

    @mock.patch("sat.changes.changerepo.changes")
    def test_load_data_calls_change_repo_as_expected(self, change_repo):
        exp_working_dir = "dummy/dir"
        self.sut.load_data(exp_working_dir, "")
        change_repo.assert_called_with(exp_working_dir, self.expected_since)

    @mock.patch("sat.changes.changerepo.changes")
    def test_analyse_creates_expected_result(self, change_repo):
        change_repo.return_value = _CHANGES

        self.sut.load_data("", "")
        result = self.sut.analyse("")

        paths = list(result[FileChanges._COLUMNS[0]])
        self.assertEqual(len(paths), 4)
        self.assertTrue(_CHANGE_PATH_1 in paths)
        self.assertTrue(_CHANGE_PATH_2 in paths)
        self.assertTrue(_CHANGE_PATH_3 in paths)
        self.assertTrue(_CHANGE_PATH_4 in paths)

        names = list(result[FileChanges._COLUMNS[1]])
        self.assertEqual(len(names), 4)
        self.assertTrue(_CHANGE_1 in names)
        self.assertTrue(_CHANGE_2 in names)
        self.assertTrue(_CHANGE_3 in names)
        self.assertTrue(_CHANGE_4 in names)

        lines_changed = list(result[FileChanges._COLUMNS[2]])
        self.assertListEqual(lines_changed, [75, 30, 20, 0])

        lines_added = list(result[FileChanges._COLUMNS[3]])
        self.assertListEqual(lines_added, [55, 10, 0, 0])

        lines_removed = list(result[FileChanges._COLUMNS[4]])
        self.assertListEqual(lines_removed, [20, 20, 20, 0])

    @mock.patch("sat.report.plot.plot_stacked_barchart")
    @mock.patch("sat.report.writer.write_dataframe_to_xls")
    def test_write_results_calls_xls_writer_as_expected(self, writer, dummy_plot):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        exp_output_folder = "dummy//folder"
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        self.sut.write_results(exp_output_folder)

        writer.assert_called_once_with(
            result,
            "changed_lines_per_file.xls",
            exp_output_folder,
            "Changes since " + self.expected_since,
        )

    @mock.patch("sat.report.plot.plot_stacked_barchart")
    @mock.patch("sat.report.writer.write_dataframe_to_xls")
    def test_write_results_calls_plot_as_expected(self, dummy_writer, plot):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        exp_output_folder = "dummy//folder"
        self.sut.load_data("", "")
        self.sut.analyse("")

        self.sut.write_results(exp_output_folder)

        plot.assert_called_once_with(
            ANY,
            "Number of changed lines",
            "Number of changed lines for most changed files since "
            + self.expected_since,
            exp_output_folder,
            "most_changed_files.pdf",
        )

    @mock.patch("sat.changes.changerepo.changes")
    @mock.patch("sat.report.plot.plot_stacked_barchart")
    @mock.patch("sat.report.writer.write_dataframe_to_xls")
    def test_write_results_plots_expected_dataframe(
        self, dummy_writer, plot, change_repo
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        change_repo.return_value = _CHANGES
        exp_output_folder = "dummy//folder"
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        exp_treemap_data = result.drop(
            columns=[FileChanges._COLUMNS[1], FileChanges._COLUMNS[2]]
        )

        self.sut.write_results(exp_output_folder)

        used_treemap_data = plot.call_args_list[0][0][0]
        assert_frame_equal(exp_treemap_data, used_treemap_data)
