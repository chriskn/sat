#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.__main__ as main
import unittest
import sat.deps.parser.projectparser as parser

import sat.deps.coupling as sut

_ROOT_LOCATION = os.path.dirname(os.path.dirname(os.path.abspath(main.__file__)))
EXAMPLE_PROJECTS_LOCATION = os.path.join(_ROOT_LOCATION, "exampleprojects")


class TestProjectCoupling(unittest.TestCase):
    def setUp(self):
        self.projects = parser.parse(EXAMPLE_PROJECTS_LOCATION, [])
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
