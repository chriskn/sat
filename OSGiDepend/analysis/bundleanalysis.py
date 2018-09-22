#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from bundle.bundleparser import BundleParser 
from bundle.bundlegraph import BundleGraph
from domain import Bundle 
import os 

class BundleAnalyser(Analysis):

    _OUTPUT_HEADER = ["Name", "Version", "Number of Dependencies", "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
    _CSV_SEPARATOR = "\t"
    _LIST_SEPARATOR = ", " 

    def getName(self):
        return "bundleDeps"
    
    def getDescription(self):
        return "Analysis OSGi bundle dependencies"

    def loadData(self, workingDir, ignoredPathSegments):
        self.logger.info("Loading bundle data...")
        bundleParser = BundleParser(workingDir, ignoredPathSegments)
        self._bundles = bundleParser.parseBundles()
        self._bundlesForExports = self._mapBundlesOnExports(self._bundles)
        self.logger.info("Found %d bundle(s)" % len(self._bundles))

    def analyse(self, workingDir, ignoredPathSegments):     
        self.logger.info("Creating dependency graph...")
        graph = BundleGraph(self._bundles, self._bundlesForExports, ignoredPathSegments)
        self.logger.info("Created dependency graph containing %d node(s) and %d edge(s)" % (len(graph.getNodes()), len(graph.getEdges())))
        self.logger.info("Searching for cycles...")
        cycles = graph.getCycles()
        graph.markCycles(cycles)
        self.logger.info("Found %d cycle(s)" % len(cycles))
        self.logger.info("Writing output to %s" % str(workingDir))
        self._cycles = cycles
        self._graph = graph

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
                cycleList = self._LIST_SEPARATOR.join(sorted([nodeLabel for nodeLabel in cycle]))
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