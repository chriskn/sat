#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import ANY
import mock


from sat.comp.analyser.packagecomp import PackageComp
from sat.comp.domain import Method, Type, Package

_PACKAGE_1 = "src.main.dummy1.domian"
_PACKAGE_2 = "src.main.dummy2.gui"
_PACKAGE_3_DUPLICATED = "converter"
_PACKAGE_4 = "interpreter"
_PACKAGE_5 = "src.main.dummy5.persistence"

_FULL_PATH_PACKAGE_1 = ("%s" * 4) % ("proj1", os.sep, _PACKAGE_1, os.sep)
_FULL_PATH_PACKAGE_2 = ("%s" * 4) % ("proj2", os.sep, _PACKAGE_2, os.sep)
_FULL_PATH_PACKAGE_3 = ("%s" * 4) % ("proj3", os.sep, _PACKAGE_3_DUPLICATED, os.sep)
_FULL_PATH_PACKAGE_4 = ("%s" * 4) % ("proj4", os.sep, _PACKAGE_4, os.sep)
_FULL_PATH_PACKAGE_5 = ("%s" * 4) % ("proj5", os.sep, _PACKAGE_5, os.sep)
_FULL_PATH_PACKAGE_6 = ("%s" * 4) % ("proj6", os.sep, _PACKAGE_3_DUPLICATED, os.sep)

_FULL_PATH_FILE_1 = _FULL_PATH_PACKAGE_1 + "dummy1.java"

_FULL_PATH_FILE_2 = _FULL_PATH_PACKAGE_2 + "dummy2.java"

_FULL_PATH_FILE_3 = _FULL_PATH_PACKAGE_3 + "dummy3.java"
_FULL_PATH_FILE_4 = _FULL_PATH_PACKAGE_4 + "dummy4.java"
_FULL_PATH_FILE_5 = _FULL_PATH_PACKAGE_4 + "dummy5.java"
_FULL_PATH_FILE_6 = _FULL_PATH_PACKAGE_5 + "dummy6.java"
_FULL_PATH_FILE_7 = _FULL_PATH_PACKAGE_6 + "dummy3.java"


_TYPE_1 = Type(
    _FULL_PATH_FILE_1,
    "dummy1",
    [Method("dummy1Method1", 10), Method("dummy1Method2", 15)],
)
_TYPE_2 = Type(
    _FULL_PATH_FILE_2,
    "dummy2",
    [Method("dummy2Method1", 5), Method("dummy2Method2", 9)],
)
_TYPE_3 = Type(
    _FULL_PATH_FILE_3,
    "dummy3",
    [Method("dummy3Method1", 0), Method("dummy3Method2", 500)],
)
_TYPE_4_EMPTY_METHODS = Type(_FULL_PATH_FILE_4, "dummy4", [])
_TYPE_5 = Type(
    _FULL_PATH_FILE_5,
    "dummy5",
    [Method("dummy5Method1", 0), Method("dummy5Method2", 42)],
)
_TYPE_6 = Type(_FULL_PATH_FILE_5, "dummy6", [Method("dummy5Method2", 500)])
_TYPE_7 = Type(_FULL_PATH_FILE_6, "dummy6", [Method("dummy7Method1", 0)])

_PACKAGES = [
    Package(_FULL_PATH_PACKAGE_1, _PACKAGE_1, [_TYPE_1]),
    Package(_FULL_PATH_PACKAGE_2, _PACKAGE_2, [_TYPE_2]),
    Package(_FULL_PATH_PACKAGE_3, _PACKAGE_3_DUPLICATED, [_TYPE_3]),
    Package(_FULL_PATH_PACKAGE_4, _PACKAGE_4, [_TYPE_4_EMPTY_METHODS]),
    Package(_FULL_PATH_PACKAGE_5, _PACKAGE_5, [_TYPE_5, _TYPE_6]),
    Package(_FULL_PATH_PACKAGE_6, _PACKAGE_3_DUPLICATED, [_TYPE_7]),
    Package(_FULL_PATH_PACKAGE_6, _PACKAGE_3_DUPLICATED, []),
]


class TestPackageComp(unittest.TestCase):
    def setUp(self):
        self.sut = PackageComp()

    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_load_data_calls_typerepo(self, package_mock_repo):
        wdir = "dummy/dir"
        ignored = "foo.bar"
        self.sut.load_data(wdir, ignored)
        package_mock_repo.assert_called_with(wdir, ignored)

    def test_name_is_methods(self):
        self.assertEqual(PackageComp.name(), "packages")

    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_analyse_creates_expected_dataframe(self, mock_package_repo):
        mock_package_repo.return_value = _PACKAGES
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        complexity = list(result["Complexity"])
        avt_comp = list(result["Average complexity by class"])
        avm_comp = list(result["Average complexity by method"])
        packages = list(result["Package"])
        paths = list(result["Path"])
        self.assertEqual(complexity, [542, 500, 25, 14, 0, 0, 0])
        self.assertEqual(avt_comp, [542 / 2, 500, 25, 14, 0, 0, 0])
        self.assertEqual(avm_comp, [542 / 3, 500 / 2, 25 / 2, 14 / 2, 0, 0, 0])
        self.assertEqual(
            packages,
            [
                _PACKAGE_5,
                _PACKAGE_3_DUPLICATED,
                _PACKAGE_1,
                _PACKAGE_2,
                _PACKAGE_4,
                _PACKAGE_3_DUPLICATED,
                _PACKAGE_3_DUPLICATED,
            ],
        )
        self.assertEqual(
            paths,
            [
                _FULL_PATH_PACKAGE_5,
                _FULL_PATH_PACKAGE_3,
                _FULL_PATH_PACKAGE_1,
                _FULL_PATH_PACKAGE_2,
                _FULL_PATH_PACKAGE_4,
                _FULL_PATH_PACKAGE_6,
                _FULL_PATH_PACKAGE_6,
            ],
        )
        self.assertEqual(len(result.columns), 5, "Columns with unexpected lengths.")

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_calls_write_data_frame(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = []
        self.sut.load_data("", "")
        self.sut.analyse("")
        odir = "result\\dir"
        self.sut.write_results(odir)
        write_xls.assert_called_with(
            ANY, "cognitive_complexity_per_package.xls", odir, "Package Complexity"
        )

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_calls_plot_treemap_for_total_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        expected_total_call = mock.call(
            ANY,
            "Cognitive complexity per package",
            odir,
            "cognitive_complexity_per_package.pdf",
            "complexity:",
        )
        plot_treemap.assert_has_calls([expected_total_call], any_order=True)

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_calls_plot_treemap_for_av_type_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        expected_avt_call = mock.call(
            ANY,
            "av class complexity per package",
            odir,
            "av_class_complexity_per_package.pdf",
            "avc complexity:",
        )
        plot_treemap.assert_has_calls([expected_avt_call], any_order=True)

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_calls_plot_treemap_for_av_method_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        expected_avm_call = mock.call(
            ANY,
            "av method complexity per package",
            odir,
            "av_method_complexity_per_package.pdf",
            "avm complexity:",
        )
        plot_treemap.assert_has_calls([expected_avm_call], any_order=True)

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_plots_expected_data_for_total_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = _PACKAGES
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        _, args1, _ = plot_treemap.mock_calls[0]
        used_dataframes = args1[0]
        complexity = list(used_dataframes["Complexity"])
        packages = list(used_dataframes["Package"])
        self.assertEqual(complexity, [542, 500, 25, 14])
        self.assertEqual(
            packages, [_PACKAGE_5, _PACKAGE_3_DUPLICATED, _PACKAGE_1, _PACKAGE_2]
        )
        self.assertEqual(
            len(used_dataframes.columns), 2, "Columns with unexpected lengths."
        )

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_plots_expected_data_for_av_class_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = _PACKAGES
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        _, args1, _ = plot_treemap.mock_calls[1]
        used_dataframes = args1[0]
        complexity = list(used_dataframes["Average complexity by class"])
        packages = list(used_dataframes["Package"])
        self.assertEqual(complexity, [542 / 2, 500, 25, 14])
        self.assertEqual(
            packages, [_PACKAGE_5, _PACKAGE_3_DUPLICATED, _PACKAGE_1, _PACKAGE_2]
        )
        self.assertEqual(
            len(used_dataframes.columns), 2, "Columns with unexpected lengths."
        )

    @mock.patch("sat.report.plot.plot_treemap")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.packagerepo.packages")
    def test_write_results_plots_expected_data_for_av_method_comp(
        self, mock_package_repo, write_xls, plot_treemap
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_package_repo.return_value = _PACKAGES
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        _, args1, _ = plot_treemap.mock_calls[2]
        used_dataframes = args1[0]
        complexity = list(used_dataframes["Average complexity by method"])
        packages = list(used_dataframes["Package"])
        self.assertEqual(complexity, [542 / 3, 500 / 2, 25 / 2, 14 / 2])
        self.assertEqual(
            packages, [_PACKAGE_5, _PACKAGE_3_DUPLICATED, _PACKAGE_1, _PACKAGE_2]
        )
        self.assertEqual(
            len(used_dataframes.columns), 2, "Columns with unexpected lengths."
        )


if __name__ == "__main__":
    unittest.main()
