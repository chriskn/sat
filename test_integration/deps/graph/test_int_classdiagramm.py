#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

from sat.deps.graph.classdiagramm import ClassDiagramm
from sat.deps.parser import projectparser
import test_integration.deps.graph.graph_test_utils as graphtest


class ClassDiagrammIntTest(unittest.TestCase):
    def setUp(self):
        projects = projectparser.parse(graphtest.EXAMPLE_PROJECTS_LOCATION, [])
        packages = []
        for project in projects:
            packages.extend(project.source_packages)
        self.packages = packages

    def test_classdiagramm_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_classdiagramm.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = ClassDiagramm(self.packages)
        sut.mark_cycles(sut.cycles(grouped=True), grouped=True)

        self.assertEqual(
            graphtest.encrypt(sut.serialize()), graphtest.encrypt(exp_graphml)
        )
