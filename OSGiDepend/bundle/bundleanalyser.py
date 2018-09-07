#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundleparser import BundleParser 
from bundle.bundlegraph import BundleGraph
from bundle. bundle import Bundle 
import os 

OUTPUT_HEADER = ["Name", "Version", "Number of Dependencies", "Exported Packages", "Imported Packages", "Required Bundles", "Path to Bundle"]
CSV_SEPARATOR = "\t"
LIST_SEPARATOR = ", " 

class BundleAnalyser:

    outputDir = "."
    cycles = None
    graph = None
    bundles = None

    def analyse(self, workingDir, ignoredPathSegments):     
        bundleParser = BundleParser(workingDir, ignoredPathSegments)
        bundles = bundleParser.parseBundles()
        bundlesForExports = self.__mapBundlesOnExports(bundles)
        print("Found %d bundle(s)" % len(bundles))
        print("Creating dependency graph...")
        graph = BundleGraph(bundles, bundlesForExports, ignoredPathSegments)
        print("Created dependency graph containing %d node(s) and %d edge(s)" % (len(graph.getNodes()), len(graph.getEdges())))
        print("Searching for cycles...")
        cycles = graph.getCycles()
        graph.markCycles(cycles)
        print("Found %d cycle(s)" % len(cycles))
        print("Writing output to %s" % str(workingDir))
        self.cycles = cycles
        self.graph = graph
        self.bundles = bundles

    def writeResults(self, outputDir):
        self.__writeCyclesToTxt(os.path.join(outputDir,"bundle_cycles.txt"), self.cycles, self.graph)
        self.__writeBundlesToCsv(os.path.join(outputDir,"bundles.csv"), self.bundles)
        self.__writeGraphToGraphMl(os.path.join(outputDir,"dependencies.graphml"), self.graph)

    def __mapBundlesOnExports(self, bundles):
        bundlesForExports = {}
        for bundle in bundles:
            for export in bundle.exportedPackages:
                bundlesForExports[export] = bundle
        return bundlesForExports

    def __writeCyclesToTxt(self, path, cylces, graph):
        with open(path, 'w') as outputFile:
            for cycle in cylces: 
                cycleList = LIST_SEPARATOR.join(sorted([graph.getNodes()[str(nodeId)].label for nodeId in cycle]))
                outputFile.write(cycleList+"\n")

    def __writeBundlesToCsv(self, path, bundles):
        with open(path, 'w') as outputFile:
            outputFile.write(CSV_SEPARATOR.join(OUTPUT_HEADER)+"\n")
            for bundle in sorted(sorted(bundles, key=lambda x: x.name),key=lambda x: x.numberOfDependencies, reverse=True):
                outputFile.write(CSV_SEPARATOR.join([bundle.name, bundle.version, str(bundle.numberOfDependencies), LIST_SEPARATOR.join(bundle.exportedPackages), LIST_SEPARATOR.join(bundle.importedPackages), LIST_SEPARATOR.join(bundle.requiredBundles), bundle.path])+"\n")

    def __writeGraphToGraphMl(self, path, graph):
        with open(path, 'w') as outputFile:
            outputFile.write(graph.serialize())