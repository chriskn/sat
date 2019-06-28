#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import pytest

from sat.deps.graph.projectgraph import ProjectGraph
from sat.deps.parser import projectparser
import test_integration.deps.graph.graph_test_utils as graphtest


class PackageGraphTest(unittest.TestCase):
    def setUp(self):
        self.projects = projectparser.parse(graphtest.EXAMPLE_PROJECTS_LOCATION, [])

    @pytest.mark.graph
    def test_packagegraph_looks_like_expected(self):
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
