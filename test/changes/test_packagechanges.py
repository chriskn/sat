#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import ANY

import mock
from pandas.util.testing import assert_frame_equal

from sat.changes.analyser.packagechanges import PackageChanges
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

_CHANGES = [
    Change(os.path.join(_ABS_PACKAGE_PATH_1, "dummy1.java"), 10, 20),
    Change(os.path.join(_ABS_PACKAGE_PATH_1_2, "dummy2.java"), 0, 20),
    Change(os.path.join(_ABS_PACKAGE_PATH_3, "dummy3.java"), 55, 20),
    Change(os.path.join(_ABS_PACKAGE_PATH_4, "dummy4.java"), 0, 0),
]


class PackageChangesTest(unittest.TestCase):
    # allow protected-access
    # pylint: disable = W0212

    def setUp(self):
        self.expected_since = "12.10.2018"
        self.sut = PackageChanges(self.expected_since)

    def test_name_is_packages(self):
        self.assertEqual(PackageChanges.name(), "packages")

    @mock.patch("sat.changes.changerepo.changes")
    def test_load_data_calls_change_repo_as_expected(self, change_repo):
        exp_working_dir = os.path.join("dummy", "dir")
        self.sut.load_data(exp_working_dir, "")
        change_repo.assert_called_with(exp_working_dir, self.expected_since)

    @mock.patch("sat.scanner.find_packages")
    def test_load_data_calls_scanner_as_expected(self, scanner):
        exp_working_dir = os.path.join("dummy", "dir2")
        exp_ignored = "test"
        self.sut.load_data(exp_working_dir, exp_ignored)
        scanner.assert_called_with(exp_working_dir, exp_ignored)

    @mock.patch("sat.scanner.find_packages")
    @mock.patch("sat.changes.changerepo.changes")
    def test_analyse_creates_expected_result(self, change_repo, scanner):
        change_repo.return_value = _CHANGES
        scanner.return_value = _REL_PACK_PATH_FOR_PACK_PATH

        self.sut.load_data("", "")
        result = self.sut.analyse("")

        paths = list(result[PackageChanges._COLUMNS[0]])
        self.assertEqual(len(paths), 5)
        self.assertTrue(_REL_PACK_PATH_1 in paths)
        self.assertTrue(_REL_PACK_PATH_1_2 in paths)
        self.assertTrue(_REL_PACK_PATH_3 in paths)
        self.assertTrue(_REL_PACK_PATH_4 in paths)
        self.assertTrue(_REL_PACK_PATH_5 in paths)

        names = list(result[PackageChanges._COLUMNS[1]])
        self.assertEqual(len(names), 5)
        self.assertTrue(_REL_PACK_PATH_1.replace(os.sep, ".") in names)
        self.assertTrue(_REL_PACK_PATH_1_2.replace(os.sep, ".") in names)
        self.assertTrue(_REL_PACK_PATH_3.replace(os.sep, ".") in names)
        self.assertTrue(_REL_PACK_PATH_4.replace(os.sep, ".") in names)
        self.assertTrue(_REL_PACK_PATH_5.replace(os.sep, ".") in names)

        lines_changed = list(result[PackageChanges._COLUMNS[2]])
        self.assertListEqual(lines_changed, [75, 30, 20, 0, 0])

        lines_added = list(result[PackageChanges._COLUMNS[3]])
        self.assertListEqual(lines_added, [55, 10, 0, 0, 0])

        lines_removed = list(result[PackageChanges._COLUMNS[4]])
        self.assertListEqual(lines_removed, [20, 20, 20, 0, 0])

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    def test_write_reults_calls_xls_writer_as_expected(self, writer, dummy_plot):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        exp_output_folder = os.path.join("dummy", "folder")
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        self.sut.write_results(exp_output_folder)

        writer.assert_called_once_with(
            result,
            "changed_lines_per_package.xls",
            exp_output_folder,
            "Changes since " + self.expected_since,
        )

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    def test_write_reults_calls_plot_as_expected(self, dummy_writer, plot):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        exp_output_folder = os.path.join("dummy", "folder")
        self.sut.load_data("", "")
        self.sut.analyse("")

        self.sut.write_results(exp_output_folder)

        plot.assert_called_once_with(
            ANY,
            "Number of changed lines per packag since " + self.expected_since,
            exp_output_folder,
            "changed_lines_per_package.pdf",
            "changes:",
        )

    @mock.patch("sat.scanner.find_packages")
    @mock.patch("sat.changes.changerepo.changes")
    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    def test_write_reults_plots_expected_dataframe(
        self, dummy_writer, plot, change_repo, scanner
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        change_repo.return_value = _CHANGES
        scanner.return_value = _REL_PACK_PATH_FOR_PACK_PATH
        exp_output_folder = "dummy//folder"
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        exp_treemap_data = result.drop(
            columns=[
                PackageChanges._COLUMNS[0],
                PackageChanges._COLUMNS[3],
                PackageChanges._COLUMNS[4],
            ]
        )
        exp_treemap_data = exp_treemap_data[
            exp_treemap_data[PackageChanges._COLUMNS[2]] > 0
        ]

        self.sut.write_results(exp_output_folder)

        used_treemap_data = plot.call_args_list[0][0][0]
        assert_frame_equal(exp_treemap_data, used_treemap_data)
