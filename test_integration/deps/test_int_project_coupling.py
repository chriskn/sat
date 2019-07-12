#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import test_integration.int_test_utils as inttest

import sat.deps.coupling as sut
from sat.deps.depsworkspace import DepsWorkspace


class TestProjectCoupling(unittest.TestCase):
    def setUp(self):
        workspace = DepsWorkspace(inttest.EXAMPLE_PROJECTS_LOCATION, [])
        self.projects = workspace.projects()
        self.expected_index = [
            "my.dummy.project5",
            "my.dummy.project4",
            "my.dummy.project3",
            "my.dummy.project2",
            "my.dummy.project1",
        ]

    def test_projet_coupling_dataframe_has_expected_index(self):
        dataframe = sut.project_coupling_dataframe(self.projects)

        self.assertListEqual(list(dataframe.index.values), self.expected_index)

    def test_projet_coupling_dataframe_has_expected_columns(self):
        dataframe = sut.project_coupling_dataframe(self.projects)

        self.assertListEqual(list(dataframe.columns.values), self.expected_index[::-1])

    def test_projet_coupling_dataframe_has_expected_values(self):
        dataframe = sut.project_coupling_dataframe(self.projects)

        self.assertListEqual(
            dataframe.values.tolist(),
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 1, 3],
                [2, 0, 0, 0, 0],
                [2, 0, 0, 0, 0],
                [2, 0, 0, 1, 0],
            ],
        )
