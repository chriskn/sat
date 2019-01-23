#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.analyser import Analyser
from deps.parser.bundleparser import BundleParser
from deps.graph.bundlegraph import BundleGraph
from deps.domain import Bundle
import os


_OUTPUT_HEADER = ["Name", "Version", "Number of Dependencies",
                  "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
_CSV_SEPARATOR = "\t"
_LIST_SEPARATOR = ", "


class BundleAnalyser(Analyser):

    @staticmethod
    def name():
        return "bundleDeps"

    def load_data(self, workingDir, ignoredPathSegments):
        self._logger.info("Loading bundle data...")
        parser = BundleParser(workingDir, ignoredPathSegments)
        self._bundles = parser.parse()
        self._bundlesForExports = self._map_bundles_on_exports(self._bundles)
        self._logger.info("Found %d bundle(s)" % len(self._bundles))

    def analyse(self, ignoredPathSegments):
        self._logger.info("Creating dependency graph...")
        graph = BundleGraph(
            self._bundles, self._bundlesForExports, ignoredPathSegments)
        self._logger.info("Created dependency graph")
        self._logger.info("Searching for cycles...")
        cycles = graph.cycles()
        graph.mark_cycles(cycles)
        self._logger.info("Found %d cycle(s)" % len(cycles))
        self._cycles = cycles
        self._graph = graph

    def write_results(self, output_dir):
        self._logger.info("Writing output to %s" % str(output_dir))
        self._write_cycles_to_txt(os.path.join(
            output_dir, "bundle_cycles.txt"))
        self._writeBundlesToCsv(os.path.join(output_dir, "bundles.csv"))
        self._writeGraphToGraphMl(os.path.join(
            output_dir, "dependencies.graphml"))

    def _map_bundles_on_exports(self, bundles):
        bundles_for_exports = {}
        for bundle in bundles:
            for export in bundle.exported_packages:
                bundles_for_exports[export] = bundle
        return bundles_for_exports

    def _write_cycles_to_txt(self, path):
        with open(path, 'w') as output_file:
            for cycle in self._cycles:
                cycleList = _LIST_SEPARATOR.join(
                    sorted([label for label in cycle]))
                output_file.write(cycleList+"\n")

    def _writeBundlesToCsv(self, path):
        with open(path, 'w') as output_file:
            output_file.write(_CSV_SEPARATOR.join(
                _OUTPUT_HEADER)+"\n")
            for bundle in sorted(sorted(self._bundles, key=lambda x: x.name), key=lambda x: x.num_dependencies, reverse=True):
                output_file.write(_CSV_SEPARATOR.join([
                    bundle.name,
                    bundle.version,
                    str(bundle.num_dependencies),
                    _LIST_SEPARATOR.join(bundle.exported_packages),
                    _LIST_SEPARATOR.join(bundle.imported_packages),
                    _LIST_SEPARATOR.join(bundle.required_bundles),
                    bundle.path])
                    + "\n")

    def _writeGraphToGraphMl(self, path):
        with open(path, 'w') as output_file:
            output_file.write(self._graph.serialize())
