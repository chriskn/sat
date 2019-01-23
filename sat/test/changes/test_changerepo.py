#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from subprocess import CalledProcessError, CompletedProcess

import mock

import changes.changerepo as sut

_PATH_TO_TESTDATA = "test\\changes\\data\\git_changes_test.log"


class TestChangeRepo(unittest.TestCase):

    def setUp(self):
        sut._changes_by_dir = dict()

    @mock.patch("changes.changerepo._parse_changes")
    def test_changes_does_run_command_twice_for_same_params(self, _parse_changes):
        workingdir = "foo"
        since = "01.01.2018"

        sut.changes(workingdir, since)
        sut.changes(workingdir, since)

        self.assertEqual(_parse_changes.call_count, 1)

    @mock.patch("changes.changerepo._run_git_command")
    def test_changes_return_expected_amount_of_changes(self, git_executer):
        git_executer.return_value = self._load_executer_testdata()
        expected_size = 53

        resulting_changes = sut.changes("", "")

        self.assertEqual(len(resulting_changes), expected_size)

    @mock.patch("subprocess.run")
    def test_changes_return_expected_changes(self, git_executer):
        test_result = CompletedProcess(
            args=[], returncode=0, stdout=self._load_executer_testdata())
        git_executer.return_value = test_result

        resulting_changes = sut.changes("", "")

        max_change = sorted(
            resulting_changes, key=lambda c: c.lines_added+c.lines_removed, reverse=True)[0]
        self._assertChange(
            max_change, 'exampleprojects\\my.dummy.project5\\src\\my\\dummy\\project5\\compl\\dummy\\ComplDummy.java', 144, 0)

        path_for_change_with_added_and_removed = 'exampleprojects\\my.dummy.project1\\META-INF\\MANIFEST2.MF'
        change_with_added_and_removed = self._get_change_by_path(
            resulting_changes, path_for_change_with_added_and_removed)[0]
        self._assertChange(change_with_added_and_removed,
                           path_for_change_with_added_and_removed, 1, 2)

        path_with_multiple_changes = 'exampleprojects\\my.dummy.project1\\META-INF\\MANIFEST.MF'
        multiple_changes_for_path = self._get_change_by_path(
            resulting_changes, path_with_multiple_changes)
        self.assertEqual(len(multiple_changes_for_path), 2)

    @mock.patch("subprocess.run", **{'side_effect': OSError()})
    def test_changes_returns_empty_list_if_oserror_occur_during_process_execution(self, executer):
        resulting_changes = sut.changes("", "")
        self.assertRaises(OSError, executer)
        self.assertEqual(len(resulting_changes), 0)

    @mock.patch("subprocess.run", **{'side_effect': CalledProcessError(returncode=1, cmd="")})
    def test_changes_returns_empty_list_if_processerror_occur_during_process_execution(self, executer):
        resulting_changes = sut.changes("", "")
        self.assertRaises(CalledProcessError, executer)
        self.assertEqual(len(resulting_changes), 0)

    def _load_executer_testdata(self):
        testfile = os.path.join(os.getcwd(), _PATH_TO_TESTDATA)
        expected_content = None
        with open(testfile, 'r') as f:
            expected_content = f.read()
        return expected_content.encode(encoding='UTF-8', errors='strict')

    def _get_change_by_path(self, changes, path):
        return [change for change in changes if change.path == path]

    def _assertChange(self, change, exp_path, exp_added, exp_removed):
        self.assertEqual(change.path, exp_path)
        self.assertEqual(change.lines_added, exp_added)
        self.assertEqual(change.lines_removed, exp_removed)
        self.assertEqual(change.total_lines, exp_added+exp_removed)
