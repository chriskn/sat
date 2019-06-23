#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import mock
from mock import Mock

import sat.changes.changeparser as sut


class TestChangeParser(unittest.TestCase):
    @mock.patch("subprocess.run")
    def test_changes_returns_process_stdout(self, executer):
        completed_process = Mock()
        executer.return_value = completed_process
        expected_stdout = ""
        completed_process.stdout = expected_stdout

        resulting_changes = sut.parse_changes("", "")

        self.assertEqual(resulting_changes, [])
