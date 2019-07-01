#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import pytest

from sat.deps.graph.bundlegraph import BundleGraph
from sat.deps.parser import bundleparser
import test_integration.deps.graph.graph_test_utils as graphtest
import test_integration.int_test_utils as inttest


class BundleGraphTest(unittest.TestCase):
    def setUp(self):
        self.bundles = bundleparser.parse(inttest.EXAMPLE_PROJECTS_LOCATION, [])

    @pytest.mark.graph
    def test_bundlegraph_looks_like_expected(self):
        exp_graphml = open(
            os.path.join(graphtest.REF_DATA_FOLDER, "ref_bundlegraph.graphml"),
            "r",
            encoding="utf-8",
        ).read()

        sut = BundleGraph(self.bundles, [])
        sut.mark_cycles(sut.cycles())

        self.assertEqual(
            graphtest.encrypt(sut.serialize()), graphtest.encrypt(exp_graphml)
        )
