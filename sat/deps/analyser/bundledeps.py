#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

import sat.app.report.writer as writer
from sat.app.execution.analyser import Analyser
from sat.deps.graph.bundlegraph import BundleGraph

_LIST_SEPARATOR = ", "
_COLUMNS = [
    "Name",
    "Version",
    "Number of Dependencies",
    "Exported Packages",
    "Imported Packages",
    "Required Bundles",
    "Path to Bundle",
]


class BundleDepsAnalyser(Analyser):
    @staticmethod
    def name():
        return "bundles"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._bundles = []
        self._cycles = []
        self._graph = None
        self._analysis_result = None

    def load_data(self):
        self._logger.info("Loading bundle data...")
        self._bundles = self._workspace.bundles()
        self._logger.info("Found %d bundle(s)", len(self._bundles))

    def analyse(self):
        self._logger.info("Creating dependency graph...")
        graph = BundleGraph(self._bundles)
        self._logger.info("Created dependency graph")
        self._logger.info("Searching for cycles...")
        cycles = graph.cycles()
        graph.mark_cycles(cycles)
        self._logger.info("Found %d cycle(s)", len(cycles))
        self._cycles = cycles
        self._graph = graph
        data = []
        for bundle in sorted(
            sorted(self._bundles, key=lambda x: x.name),
            key=lambda x: x.num_dependencies,
            reverse=True,
        ):
            data.append(
                (
                    bundle.name,
                    bundle.version,
                    str(bundle.num_dependencies),
                    _LIST_SEPARATOR.join(bundle.exported_packages),
                    _LIST_SEPARATOR.join(bundle.imported_packages),
                    _LIST_SEPARATOR.join(bundle.required_bundles),
                    bundle.abs_path,
                )
            )
        self._analysis_result = pd.DataFrame(data=data, columns=_COLUMNS)
        return self._analysis_result

    def write_results(self, output_dir):
        self._logger.info("Writing output to %s", str(output_dir))
        writer.write_cycles_to_txt(
            os.path.join(output_dir, "bundle_cycles.txt"), self._cycles
        )
        writer.write_dataframe_to_xls(
            self._analysis_result, "bundles.xls", output_dir, "Bundles"
        )
        writer.write_graphml(
            os.path.join(output_dir, "dependencies.graphml"), self._graph
        )
