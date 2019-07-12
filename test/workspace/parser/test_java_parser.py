#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import mock
import sat.app.workspace.parser.java_parser as sut
from javalang.parser import JavaSyntaxError

# unused mock objects
# pylint: disable=W0613


class TestJavaParser(unittest.TestCase):
    @mock.patch("builtins.open", side_effect=FileNotFoundError())
    def test_parse_return_none_if_file_not_found(self, mock_open):
        self.assertIsNone(sut.parse(""))

    @mock.patch("builtins.open", side_effect=JavaSyntaxError(""))
    def test_parse_return_none_if_syntax_error_occurs(self, mock_open):
        self.assertIsNone(sut.parse(""))
