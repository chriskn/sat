#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import mock

import sat.comp.repo.packagerepo as sut
from sat.comp.domain import Type


class TestPackageRepo(unittest.TestCase):
    def tearDown(self):
        # pylint: disable =  W0212
        sut._packages = dict()

    @mock.patch("sat.comp.parser.packageparser.parse_packages")
    def test_packages_not_calls_parse_packages_twice_for_same_input(
        self, parse_packages
    ):
        workingdir = "foo"
        ignored = ["bar", "blub", "foo"]
        sut.packages(workingdir, ignored)
        sut.packages(workingdir, ignored)
        self.assertEqual(parse_packages.call_count, 1)

    @mock.patch("sat.comp.parser.packageparser.parse_packages")
    def test_packages_calls_parse_packages_depending_on_dir_and_ignored(
        self, parse_packages
    ):
        workingdir = "foo"
        ignored = ["bar", "", "foo"]
        sut.packages(workingdir, ignored)
        # duplicate
        sut.packages(workingdir, ignored)
        sut.packages(workingdir, ignored + ["another"])
        sut.packages(workingdir + "another", ignored)
        self.assertEqual(parse_packages.call_count, 3)

    @mock.patch("sat.comp.parser.packageparser.parse_packages")
    def test_packages_calls_parse_packages(self, parse_packages):
        sut.packages("", "")
        self.assertEqual(parse_packages.call_count, 1)

    @mock.patch("sat.scanner.find_packages", return_value=dict())
    def test_scanner_is_called_with_expected_params(self, scanner):
        workingdir = "blub"
        ignored = ["bar"]
        sut.packages(workingdir, ignored)
        self.assertEqual(scanner.call_count, 1)
        scanner.assert_called_with(workingdir, ignored)

    @mock.patch("sat.comp.parser.typeparser.parse")
    def test_parser_is_not_called_if_no_file_found(self, parser):
        sut.packages("", "")
        self.assertEqual(parser.call_count, 0)

    @mock.patch("sat.scanner.find_packages")
    @mock.patch("sat.comp.repo.typerepo.types")
    def test_parser_creates_expected_packages(self, repo, scanner):
        scanner_result = {
            "proj1//a1/b1//": "a1" + os.sep + "b1",
            # single slash after proj2 is by intention
            "proj2/a2//": "a2",
            "proj3//a2//": "a2",
        }
        types = [
            Type("proj1//a1/b1//dummy.java", "", []),
            Type("proj2//a2/dummy.java", "", []),
            Type("proj3//a2/dummy.java", "", []),
        ]
        scanner.return_value = scanner_result
        repo.return_value = types

        packages = sut.packages("path", "")

        self.assertEqual(len(packages), 3)
        package1 = packages[0]
        package2 = packages[1]
        package3 = packages[2]
        self._assert_package(package1, "proj1//a1/b1//", "a1.b1", types[0].path)
        self._assert_package(package2, "proj2/a2//", "a2", types[1].path)
        self._assert_package(package3, "proj3//a2//", "a2", types[2].path)

    def _assert_package(self, package, exp_path, exp_name, exp_type):
        self.assertEqual(package.path, exp_path)
        self.assertEqual(package.name, exp_name)
        self.assertEqual(package.types[0].path, exp_type)
