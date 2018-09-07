#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundleparser import BundleParser 
from bundle.bundlegraph import BundleGraph
from bundle. bundle import Bundle 
import os 

class BundleAnalyser:

    _OUTPUT_HEADER = ["Name", "Version", "Number of Dependencies", "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
    _CSV_SEPARATOR = "\t"
    _LIST_SEPARATOR = ", " 
    
    _cycles = None
    _graph = None
    _bundles = None

    def analyse(self, workingDir, ignoredPathSegments):     
        bundleParser = BundleParser(workingDir, ignoredPathSegments)
        bundles = bundleParser.parseBundles()
        bundlesForExports = self._mapBundlesOnExports(bundles)
        print("Found %d bundle(s)" % len(bundles))
        print("Creating dependency graph...")
        graph = BundleGraph(bundles, bundlesForExports, ignoredPathSegments)
        print("Created dependency graph containing %d node(s) and %d edge(s)" % (len(graph.getNodes()), len(graph.getEdges())))
        print("Searching for cycles...")
        cycles = graph.getCycles()
        graph.markCycles(cycles)
        print("Found %d cycle(s)" % len(cycles))
        print("Writing output to %s" % str(workingDir))
        self._cycles = cycles
        self._graph = graph
        self._bundles = bundles

    def writeResults(self, outputDir):
        self._writeCyclesToTxt(os.path.join(outputDir,"bundle_cycles.txt"))
        self._writeBundlesToCsv(os.path.join(outputDir,"bundles.csv"))
        self._writeGraphToGraphMl(os.path.join(outputDir,"dependencies.graphml"))

    def _mapBundlesOnExports(self, bundles):
        bundlesForExports = {}
        for bundle in bundles:
            for export in bundle.exportedPackages:
                bundlesForExports[export] = bundle
        return bundlesForExports

    def _writeCyclesToTxt(self, path):
        with open(path, 'w') as outputFile:
            for cycle in self._cycles: 
                cycleList = self._LIST_SEPARATOR.join(sorted([self._graph.getNodes()[str(nodeId)].label for nodeId in cycle]))
                outputFile.write(cycleList+"\n")

    def _writeBundlesToCsv(self, path):
        with open(path, 'w') as outputFile:
            outputFile.write(self._CSV_SEPARATOR.join(self._OUTPUT_HEADER)+"\n")
            for bundle in sorted(sorted(self._bundles, key=lambda x: x.name),key=lambda x: x.numberOfDependencies, reverse=True):
                outputFile.write(self._CSV_SEPARATOR.join([
                    bundle.name, 
                    bundle.version, 
                    str(bundle.numberOfDependencies), 
                    self._LIST_SEPARATOR.join(bundle.exportedPackages),
                    self._LIST_SEPARATOR.join(bundle.importedPackages), 
                    self._LIST_SEPARATOR.join(bundle.requiredBundles), 
                    bundle.path])
                +"\n")

    def _writeGraphToGraphMl(self, path):
        with open(path, 'w') as outputFile:
            outputFile.write(self._graph.serialize())