#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pytest

import test_integration.deps.graph.graph_test_utils as graphtest
import test_integration.int_test_utils as inttest
from sat.deps.depsworkspace import DepsWorkspace
from sat.deps.graph.classdiagramm import ClassDiagramm


class ClassDiagrammIntTest(unittest.TestCase):
    def setUp(self):
        projects = DepsWorkspace(inttest.EXAMPLE_PROJECTS_LOCATION, []).projects()
        packages = []
        for project in projects:
            packages.extend(project.packages)
        self.packages = packages

    @pytest.mark.graph
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

    @pytest.mark.graph
    def test_cycle_classdiagramm_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_cycle_classdiagramm.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = ClassDiagramm(self.packages)
        cycles = sut.cycles(grouped=True)
        sut.mark_cycles(cycles, grouped=True)

        cgraph = sut.cycle_graph(cycles)

        self.assertEqual(
            graphtest.encrypt(cgraph.serialize()), graphtest.encrypt(exp_graphml)
        )
