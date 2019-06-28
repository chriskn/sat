#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import pytest

from sat.deps.graph.packagegraph import PackageGraph
from sat.deps.parser import projectparser
import test_integration.deps.graph.graph_test_utils as graphtest


class PackageGraphTest(unittest.TestCase):
    def setUp(self):
        projects = projectparser.parse(graphtest.EXAMPLE_PROJECTS_LOCATION, [])
        packages = []
        for project in projects:
            packages.extend(project.source_packages)
        self.packages = packages

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
