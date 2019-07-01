#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from sat.app.analyser import Analyser

import sat.deps.parser.bundleparser as parser
import sat.report.writer as writer
from sat.deps.graph.bundlegraph import BundleGraph

_CSV_OUTPUT_HEADER = [
    "Name",
    "Version",
    "Number of Dependencies",
    "Exported Packages",
    "Imported Packages",
    "Required Bundles",
    "Path to Bundle",
]


class BundleAnalyser(Analyser):
    @staticmethod
    def name():
        return "bundleDeps"

    def __init__(self):
        self._bundles = []
        self._cycles = []
        self._bundles_for_exports = {}
        self._graph = None

    def load_data(self, working_dir, ignored_path_segments):
        self._logger.info("Loading bundle data...")
        self._bundles = parser.parse(working_dir, ignored_path_segments)
        self._logger.info("Found %d bundle(s)", len(self._bundles))

    def analyse(self, ignored_path_segments):
        self._logger.info("Creating dependency graph...")
        graph = BundleGraph(self._bundles, ignored_path_segments)
        self._logger.info("Created dependency graph")
        self._logger.info("Searching for cycles...")
        cycles = graph.cycles()
        graph.mark_cycles(cycles)
        self._logger.info("Found %d cycle(s)", len(cycles))
        self._cycles = cycles
        self._graph = graph

    def write_results(self, output_dir):
        self._logger.info("Writing output to %s", str(output_dir))
        writer.write_cycles_to_txt(
            os.path.join(output_dir, "bundle_cycles.txt"), self._cycles
        )
        writer.write_bundles_to_csv(
            os.path.join(output_dir, "bundles.csv"), self._bundles, _CSV_OUTPUT_HEADER
        )
        writer.write_graphml(
            os.path.join(output_dir, "dependencies.graphml"), self._graph
        )
