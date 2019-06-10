#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from app.analyser import Analyser

import deps.parser.bundleparser as parser
from deps.graph.bundlegraph import BundleGraph

_OUTPUT_HEADER = [
    "Name",
    "Version",
    "Number of Dependencies",
    "Exported Packages",
    "Imported Packages",
    "Required Bundles",
    "Path to Bundle",
]
_CSV_SEPARATOR = "\t"
_LIST_SEPARATOR = ", "


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
        self._bundles_for_exports = _map_bundles_on_exports(self._bundles)
        self._logger.info("Found %d bundle(s)", len(self._bundles))

    def analyse(self, ignored_path_segments):
        self._logger.info("Creating dependency graph...")
        graph = BundleGraph(
            self._bundles, self._bundles_for_exports, ignored_path_segments
        )
        self._logger.info("Created dependency graph")
        self._logger.info("Searching for cycles...")
        cycles = graph.cycles()
        graph.mark_cycles(cycles)
        self._logger.info("Found %d cycle(s)", len(cycles))
        self._cycles = cycles
        self._graph = graph

    def write_results(self, output_dir):
        self._logger.info("Writing output to %s", str(output_dir))
        _write_cycles_to_txt(
            os.path.join(output_dir, "bundle_cycles.txt"), self._cycles
        )
        _write_bundles_to_csv(os.path.join(output_dir, "bundles.csv"), self._bundles)
        _write_graph_to_graphml(
            os.path.join(output_dir, "dependencies.graphml"), self._graph
        )


def _map_bundles_on_exports(bundles):
    bundles_for_exports = {}
    for bundle in bundles:
        for export in bundle.exported_packages:
            bundles_for_exports[export] = bundle
    return bundles_for_exports


def _write_cycles_to_txt(path, cycles):
    with open(path, "w") as output_file:
        for cycle in cycles:
            cycle_list = _LIST_SEPARATOR.join(sorted([label for label in cycle]))
            output_file.write(cycle_list + "\n")


def _write_bundles_to_csv(path, bundles):
    with open(path, "w") as output_file:
        output_file.write(_CSV_SEPARATOR.join(_OUTPUT_HEADER) + "\n")
        for bundle in sorted(
            sorted(bundles, key=lambda x: x.name),
            key=lambda x: x.num_dependencies,
            reverse=True,
        ):
            output_file.write(
                _CSV_SEPARATOR.join(
                    [
                        bundle.name,
                        bundle.version,
                        str(bundle.num_dependencies),
                        _LIST_SEPARATOR.join(bundle.exported_packages),
                        _LIST_SEPARATOR.join(bundle.imported_packages),
                        _LIST_SEPARATOR.join(bundle.required_bundles),
                        bundle.path,
                    ]
                )
                + "\n"
            )


def _write_graph_to_graphml(path, graph):
    with open(path, "w") as output_file:
        output_file.write(graph.serialize())
