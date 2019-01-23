#!/usr/bin/env python
# -*- coding: utf-8 -*-

import comp.repo.typerepo as sut
import unittest
import mock


class TestTypeRepo(unittest.TestCase):

    def tearDown(self):
        sut._types = dict()

    @mock.patch("comp.repo.typerepo._parse_types")
    def test_types_not_calls__parse_types_twice_for_same_input(self, _parse_types):
        workingdir = "foo"
        ignored = ["bar", "", "foo"]
        sut.types(workingdir, ignored)
        sut.types(workingdir, ignored)
        self.assertEqual(_parse_types.call_count, 1)

    @mock.patch("comp.repo.typerepo._parse_types")
    def test_types_calls__parse_types_depending_on_dir_and_ignored(self, _parse_types):
        workingdir = "foo"
        ignored = ["bar", "", "foo"]
        sut.types(workingdir, ignored)
        sut.types(workingdir, ignored)
        sut.types(workingdir, ignored+["another"])
        sut.types(workingdir+"another", ignored)
        self.assertEqual(_parse_types.call_count, 3)

    @mock.patch("comp.repo.typerepo._parse_types")
    def test_types_calls__parse_types(self, _parse_types):
        sut.types("", "")
        self.assertEqual(_parse_types.call_count, 1)

    @mock.patch("scanner.find_java_source_files", return_value=[])
    def test_scanner_is_called_with_right_params(self, scanner):
        workingdir = "blub"
        ignored = ["bar"]
        sut.types(workingdir, ignored)
        self.assertEqual(scanner.call_count, 1)
        scanner.assert_called_with(workingdir, ignored)

    @mock.patch("scanner.find_java_source_files", return_value=[])
    @mock.patch("comp.typeparser.parse")
    def test_parser_is_not_called_if_no_file_found(self, parser, scanner):
        sut.types("", "")
        self.assertEqual(parser.call_count, 0)

    @mock.patch("scanner.find_java_source_files")
    @mock.patch("comp.typeparser.parse")
    def test_parser_is_called_for_all_found_files(self, parser, scanner):
        params = ["bar", "3443.java", "foo"]
        expected_calls = [mock.call(exp) for exp in params]
        scanner.return_value = params

        sut.types("", "")

        self.assertEqual(parser.call_count, 3)
        self.assertEqual(expected_calls, parser.call_args_list)
