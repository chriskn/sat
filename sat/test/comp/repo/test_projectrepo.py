#!/usr/bin/env python
# -*- coding: utf-8 -*-

import comp.repo.projectrepo as sut
from comp.domain import Package
import unittest
import mock
import os


class TestProjectRepo(unittest.TestCase):

    def tearDown(self):
        sut._projects = dict()

    @mock.patch("comp.repo.projectrepo._parse_projects")
    def test_projects_not_calls__parse_projects_twice_for_same_input(self, _parse_projects):
        workingdir = "dir"
        ignored = ["bar", "", "foo"]
        sut.projects(workingdir, ignored)
        sut.projects(workingdir, ignored)
        self.assertEqual(_parse_projects.call_count, 1)

    @mock.patch("comp.repo.projectrepo._parse_projects")
    def test_projects_calls__parse_projects_depending_on_dir_and_ignored(self, _parse_projects):
        workingdir = "foo"
        ignored = ["bar", "", "foo"]
        sut.projects(workingdir, ignored)
        # duplicate
        sut.projects(workingdir, ignored)
        sut.projects(workingdir, ignored+["another"])
        sut.projects(workingdir+"another", ignored)
        self.assertEqual(_parse_projects.call_count, 3)

    @mock.patch("comp.repo.projectrepo._parse_projects")
    def test_projects_calls__parse_projects(self, _parse_projects):
        sut.projects("someworkingdir", "")
        self.assertEqual(_parse_projects.call_count, 1)

    @mock.patch("scanner.find_projects", return_value=dict())
    @mock.patch("comp.repo.packagerepo.packages", return_value=dict())
    def test_scanner_is_called_with_expected_params(self, scanner, packages):
        workingdir = "test"
        ignored = ["bar"]
        sut.projects(workingdir, ignored)
        self.assertEqual(scanner.call_count, 1)
        scanner.assert_called_with(workingdir, ignored)

    @mock.patch("scanner.find_projects", return_value=dict())
    @mock.patch("comp.typeparser.parse")
    def test_parser_is_not_called_if_no_file_found(self, parser, scanner):
        sut.projects("", "")
        self.assertEqual(parser.call_count, 0)

    @mock.patch("scanner.find_projects")
    @mock.patch("comp.repo.packagerepo.packages")
    def test_parser_creates_expected_projects(self, packagerepo, scanner):
        scanner_result = {
            "foo//bar//proj1//a1/b1//": "a1"+os.sep+"b1",
            # single slash after proj2 is by intention
            "bar//proj2/a2//": "a2",
            "proj3//a2//": "a2"
        }
        packages = [
            Package("foo//bar//proj1//a1/b1//package1", "package1", []),
            Package("bar//proj2/a2//package2", "package2", []),
            Package("proj3//a2//package3", "package3", [])
        ]

        scanner.return_value = scanner_result
        packagerepo.return_value = packages

        projects = sut.projects("", "")

        self.assertEqual(len(projects), 3)
        project1 = projects[0]
        project2 = projects[1]
        project3 = projects[2]
        self._assertProject(
            project1, "foo//bar//proj1//a1/b1//", "a1.b1", packages[0])
        self._assertProject(project2, "bar//proj2/a2//", "a2", packages[1])
        self._assertProject(project3, "proj3//a2//", "a2", packages[2])
        print(projects)

    def _assertProject(self, project, exp_path, exp_name, exp_package):
        self.assertEqual(project.path, exp_path)
        self.assertEqual(project.name, exp_name)
        self.assertEqual(project.packages[0], exp_package)
