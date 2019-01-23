#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import ANY
import mock

import javalang
from javalang.tree import ConstructorDeclaration, MethodDeclaration

from comp.analyser.projectcomp import ProjectComp
from comp.domain import Method, Type, Package, Project
from collections import OrderedDict

import os

_PROJ_PATH_1 = "..\\my\\dummy\\path\\proj1"
_PROJ_PATH_2 = "..\\my\\dummy\\proj2"
_PROJ_PATH_3 = "..\\my\\proj3"

_PACKAGE_1 = "src.main.dummy1.domian"
_PACKAGE_2 = "src.main.dummy2.gui"
_PACKAGE_3_DUPLICATED = "converter"
_PACKAGE_4 = "interpreter"
_PACKAGE_5 = "src.main.dummy5.persistence"

_FULL_PATH_PACKAGE_1 = ("%s"*4) % (_PROJ_PATH_1, os.sep, _PACKAGE_1, os.sep)
_FULL_PATH_PACKAGE_2 = ("%s"*4) % (_PROJ_PATH_1, os.sep, _PACKAGE_2, os.sep)
_FULL_PATH_PACKAGE_3 = ("%s"*4) % (_PROJ_PATH_2, os.sep, _PACKAGE_3_DUPLICATED, os.sep)
_FULL_PATH_PACKAGE_4 = ("%s"*4) % (_PROJ_PATH_2, os.sep, _PACKAGE_4, os.sep)
_FULL_PATH_PACKAGE_5 = ("%s"*4) % (_PROJ_PATH_2, os.sep, _PACKAGE_5, os.sep)
_FULL_PATH_PACKAGE_6 = ("%s"*4) % (_PROJ_PATH_3, os.sep, _PACKAGE_3_DUPLICATED, os.sep)

_FULL_PATH_FILE_1 = _FULL_PATH_PACKAGE_1+"dummy1.java"
_FULL_PATH_FILE_2 = _FULL_PATH_PACKAGE_2+"dummy2.java"
_FULL_PATH_FILE_3 = _FULL_PATH_PACKAGE_3+"dummy3.java"
_FULL_PATH_FILE_4 = _FULL_PATH_PACKAGE_4+"dummy4.java"
_FULL_PATH_FILE_5 = _FULL_PATH_PACKAGE_4+"dummy5.java"
_FULL_PATH_FILE_6 = _FULL_PATH_PACKAGE_5+"dummy6.java"
_FULL_PATH_FILE_7 = _FULL_PATH_PACKAGE_6+"dummy3.java"

_TYPE_1 = Type(_FULL_PATH_FILE_1, "dummy1", [Method(
    "dummy1Method1", 10), Method("dummy1Method2", 15)])
_TYPE_2 = Type(_FULL_PATH_FILE_2, "dummy2", [Method(
    "dummy2Method1", 5), Method("dummy2Method2", 9)])
_TYPE_3 = Type(_FULL_PATH_FILE_3, "dummy3", [Method(
    "dummy3Method1", 0), Method("dummy3Method2", 500)])
_TYPE_4_EMPTY_METHODS = Type(_FULL_PATH_FILE_4, "dummy4", [])
_TYPE_5 = Type(_FULL_PATH_FILE_5, "dummy5", [Method(
    "dummy5Method1", 0), Method("dummy5Method2", 42)])
_TYPE_6 = Type(_FULL_PATH_FILE_5, "dummy6", [Method("dummy5Method2", 500)])
_TYPE_7 = Type(_FULL_PATH_FILE_6, "dummy6", [Method("dummy7Method1", 0)])

_PACKAGE_1 = Package(_FULL_PATH_PACKAGE_1, _PACKAGE_1, [_TYPE_1])
_PACKAGE_2 = Package(_FULL_PATH_PACKAGE_2, _PACKAGE_2, [_TYPE_2])
_PACKAGE_3 = Package(_FULL_PATH_PACKAGE_3, _PACKAGE_3_DUPLICATED, [_TYPE_3])
_PACKAGE_4 = Package(_FULL_PATH_PACKAGE_4, _PACKAGE_4, [_TYPE_4_EMPTY_METHODS])
_PACKAGE_5 = Package(_FULL_PATH_PACKAGE_5, _PACKAGE_5, [_TYPE_5, _TYPE_6])
_PACKAGE_6 = Package(_FULL_PATH_PACKAGE_6, _PACKAGE_3_DUPLICATED, [_TYPE_7])
_PACKAGE_7 = Package(_FULL_PATH_PACKAGE_6, _PACKAGE_3_DUPLICATED, [])


_PROJECTS = [
    Project(_PROJ_PATH_1 , "proj1", [_PACKAGE_1, _PACKAGE_2]),
    Project(_PROJ_PATH_2 , "proj2", [_PACKAGE_3, _PACKAGE_4, _PACKAGE_5]),
    Project(_PROJ_PATH_3 , "proj3", [_PACKAGE_6, _PACKAGE_7])
]


class TestPackageComp(unittest.TestCase):

    def setUp(self):
        self.sut = ProjectComp()

    @mock.patch("comp.repo.projectrepo.projects")
    def test_load_data_calls_typerepo(self, project_mock_repo):
        wdir = "dummy/dir"
        ignored = "foo.bar"
        self.sut.load_data(wdir, ignored)
        project_mock_repo.assert_called_with(wdir, ignored)

    def test_name_is_methods(self):
        self.assertEqual(ProjectComp.name(), "projects")

    @mock.patch("comp.repo.projectrepo.projects")
    def test_analyse_creates_expected_dataframe(self, mock_project_repo):
        mock_project_repo.return_value = _PROJECTS
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        complexity = list(result['Complexity'])
        projects = list(result['Project'])
        paths = list(result['Path'])
        self.assertEqual(complexity, [1042, 39, 0])
        self.assertEqual(projects, ["proj2", "proj1", "proj3"])
        self.assertEqual(paths, [_PROJ_PATH_2, _PROJ_PATH_1, _PROJ_PATH_3])
        self.assertEqual(len(result.columns), 3,
                         "Columns with unexpected lengths.")

    @mock.patch("plot.plot_treemap")
    @mock.patch("xls.write_data_frame")
    @mock.patch("comp.repo.projectrepo.projects")
    def test_write_results_calls_write_data_frame(self, mock_project_repo, write_xls, plot_treemap):
        mock_project_repo.return_value = []
        self.sut.load_data("", "")
        self.sut.analyse("")
        odir = "result\\dir"
        self.sut.write_results(odir)
        write_xls.assert_called_with(
            ANY, "cognitive_complexity_per_project.xls", odir, "Project Complexity")

    @mock.patch("plot.plot_treemap")
    @mock.patch("xls.write_data_frame")
    @mock.patch("comp.repo.projectrepo.projects")
    def test_write_results_calls_plot_treemap_for_total_comp(self, mock_project_repo, write_xls, plot_treemap):
        mock_project_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        expected_total_call = mock.call(
            ANY, "Cognitive complexity per project", odir, "cognitive_complexity_per_project.pdf", "complexity:")
        plot_treemap.assert_has_calls([expected_total_call], any_order=True)

  
    @mock.patch("plot.plot_treemap")
    @mock.patch("xls.write_data_frame")
    @mock.patch("comp.repo.projectrepo.projects")
    def test_write_results_plots_expected_data_for_total_comp(self, mock_project_repo, write_xls, plot_treemap):
        mock_project_repo.return_value = _PROJECTS
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        _, args1, _ = plot_treemap.mock_calls[0]
        used_dataframes = args1[0]
        complexity = list(used_dataframes['Complexity'])
        projects = list(used_dataframes['Project'])
        self.assertEqual(complexity, [1042, 39])
        self.assertEqual(projects, ["proj2", "proj1"])
        self.assertEqual(len(used_dataframes.columns), 2,
                          "Columns with unexpected lengths.")

  
if __name__ == '__main__':
    unittest.main()
