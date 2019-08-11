#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import test_integration.int_test_utils as inttest
from sat.app.workspace.workspace import Workspace


class TestWorkspace(unittest.TestCase):
    def test_packages_for_projects_equal_packages_for_workspace_for_root(self):
        sut = Workspace(inttest.EXAMPLE_PROJECTS_LOCATION, [])
        projects = sut.projects()
        packages_for_projects = []
        for project in projects:
            packages_for_projects.extend(project.packages)
        packages = sut.packages()

        for index in range(0, len(packages)):
            self.assertListEqual(
                [sfile.abs_path for sfile in packages_for_projects[index].sourcefiles],
                [sfile.abs_path for sfile in packages[index].sourcefiles],
            )
        for index in range(0, len(packages)):
            self.assertListEqual(
                [sfile.rel_path for sfile in packages_for_projects[index].sourcefiles],
                [sfile.rel_path for sfile in packages[index].sourcefiles],
            )
        for index in range(0, len(packages)):
            self.assertListEqual(
                [sfile.name for sfile in packages_for_projects[index].sourcefiles],
                [sfile.name for sfile in packages[index].sourcefiles],
            )
