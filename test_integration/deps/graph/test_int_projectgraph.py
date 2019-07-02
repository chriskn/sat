#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import pytest

from sat.deps.graph.projectgraph import ProjectGraph
from sat.deps.parser import projectparser
import test_integration.deps.graph.graph_test_utils as graphtest
import test_integration.int_test_utils as inttest


class PackageGraphTest(unittest.TestCase):
    def setUp(self):
        self.projects = projectparser.parse(inttest.EXAMPLE_PROJECTS_LOCATION, [])

    @pytest.mark.graph
    def test_projectgraph_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_projectgraph.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = ProjectGraph(self.projects)
        sut.mark_cycles(sut.cycles())

        self.assertEqual(
            graphtest.encrypt(sut.serialize()), graphtest.encrypt(exp_graphml)
        )

    def test_cycle_projectgraph_looks_like_expected(self):
        exp_empty_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_cycle_projectgraph.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = ProjectGraph(self.projects)
        cycles = sut.cycles()
        sut.mark_cycles(cycles)
        proj_cycle_graph = sut.cycle_graph(cycles)

        self.assertEqual(
            graphtest.encrypt(proj_cycle_graph.serialize()),
            graphtest.encrypt(exp_empty_graphml),
        )
