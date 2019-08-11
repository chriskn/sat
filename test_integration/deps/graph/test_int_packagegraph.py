#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pytest

import test_integration.deps.graph.graph_test_utils as graphtest
import test_integration.int_test_utils as inttest
from sat.deps.depsworkspace import DepsWorkspace
from sat.deps.graph.packagegraph import PackageGraph


class PackageGraphTest(unittest.TestCase):
    def setUp(self):

        self.packages = DepsWorkspace(inttest.EXAMPLE_PROJECTS_LOCATION, []).packages()

    @pytest.mark.graph
    def test_packagegraph_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_packagegraph.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = PackageGraph(self.packages)
        sut.mark_cycles(sut.cycles())

        graphtest.write_test_graph(sut, "test_packagegraph.graphml")

        self.assertEqual(
            graphtest.encrypt(sut.serialize()), graphtest.encrypt(exp_graphml)
        )

    @pytest.mark.graph
    def test_cycle_packagegraph_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_cycle_packagegraph.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = PackageGraph(self.packages)
        cycles = sut.cycles()
        sut.mark_cycles(cycles)
        pcyclegraph = sut.cycle_graph(cycles)

        self.assertEqual(
            graphtest.encrypt(pcyclegraph.serialize()), graphtest.encrypt(exp_graphml)
        )
