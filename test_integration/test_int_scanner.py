#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sat.scanner as sut
import test_integration.int_test_utils as inttest
import os


class TestIntScanner(unittest.TestCase):
    def test_find_projects_finds_all_projects(self):
        project_dirs = sut.find_projects(inttest.EXAMPLE_PROJECTS_LOCATION, [])

        exp_proj_dirs = {
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION, "my.dummy.project%s" % index
            ): "my.dummy.project%s"
            % index
            for index in range(1, len(project_dirs) + 1)
        }

        self.assertListEqual(list(project_dirs.values()), list(exp_proj_dirs.values()))
        self.assertListEqual(list(project_dirs.keys()), list(exp_proj_dirs.keys()))

    def test_find_projects_ignores_project_names(self):
        project_dirs = sut.find_projects(
            inttest.EXAMPLE_PROJECTS_LOCATION, ["project4", "project5"]
        )

        exp_proj_dirs = {
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION, "my.dummy.project%s" % index
            ): "my.dummy.project%s"
            % index
            for index in range(1, len(project_dirs) + 1)
        }

        self.assertListEqual(list(project_dirs.keys()), list(exp_proj_dirs.keys()))

    def test_find_projects_ignores_path_segments(self):
        project_dirs = sut.find_projects(inttest.EXAMPLE_PROJECTS_LOCATION, ["sample"])

        self.assertEqual(len(project_dirs.keys()), 0)

    def test_find_packages_finds_all_packages(self):
        package_dirs = sut.find_packages(inttest.EXAMPLE_PROJECTS_LOCATION, [])

        exp_package_dirs = {
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project1",
                "src",
                "my",
                "dummy",
                "project1",
                "api",
            ): "my\\dummy\\project1\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project1",
                "src",
                "my",
                "dummy",
                "project1",
                "impl",
            ): "my\\dummy\\project1\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project2",
                "src",
                "my",
                "dummy",
                "project2",
                "api",
            ): "my\\dummy\\project2\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project2",
                "src",
                "my",
                "dummy",
                "project2",
                "impl",
            ): "my\\dummy\\project2\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project3",
                "src",
                "my",
                "dummy",
                "project3",
                "impl",
            ): "my\\dummy\\project3\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project4",
                "src",
                "my",
                "dummy",
                "project4",
                "api",
            ): "my\\dummy\\project4\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project4",
                "src",
                "my",
                "dummy",
                "project4",
                "impl",
            ): "my\\dummy\\project4\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project5",
                "src",
                "my",
                "dummy",
                "project5",
                "domain",
            ): "my\\dummy\\project5\\domain",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project5",
                "test",
                "my",
                "dummy",
                "project5",
                "domain",
            ): "my\\dummy\\project5\\domain",
        }

        self.assertListEqual(
            list(package_dirs.values()), list(exp_package_dirs.values())
        )
        self.assertListEqual(list(package_dirs.keys()), list(exp_package_dirs.keys()))

    def test_find_packages_ignores_packages(self):
        package_dirs = sut.find_packages(inttest.EXAMPLE_PROJECTS_LOCATION, ["test"])

        exp_package_dirs = {
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project1",
                "src",
                "my",
                "dummy",
                "project1",
                "api",
            ): "my\\dummy\\project1\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project1",
                "src",
                "my",
                "dummy",
                "project1",
                "impl",
            ): "my\\dummy\\project1\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project2",
                "src",
                "my",
                "dummy",
                "project2",
                "api",
            ): "my\\dummy\\project2\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project2",
                "src",
                "my",
                "dummy",
                "project2",
                "impl",
            ): "my\\dummy\\project2\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project3",
                "src",
                "my",
                "dummy",
                "project3",
                "impl",
            ): "my\\dummy\\project3\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project4",
                "src",
                "my",
                "dummy",
                "project4",
                "api",
            ): "my\\dummy\\project4\\api",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project4",
                "src",
                "my",
                "dummy",
                "project4",
                "impl",
            ): "my\\dummy\\project4\\impl",
            os.path.join(
                inttest.EXAMPLE_PROJECTS_LOCATION,
                "my.dummy.project5",
                "src",
                "my",
                "dummy",
                "project5",
                "domain",
            ): "my\\dummy\\project5\\domain",
        }

        self.assertListEqual(
            list(package_dirs.values()), list(exp_package_dirs.values())
        )
        self.assertListEqual(list(package_dirs.keys()), list(exp_package_dirs.keys()))
