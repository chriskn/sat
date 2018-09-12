#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bundle.bundle import Bundle
from repr import Graph

class BundleGraph(Graph):

    _graph = Graph()
    
    _WHITE = "#FFFFFF"
    _MIN_NODE_SIZE = 50
    _MAX_NODE_SIZE = 200
    
    def __init__(self, bundles, bundlesForExports, ignoredPathSegments):
        self.bundles = bundles
        self.bundlesForExports = bundlesForExports
        self.ignoredPathSegments = ignoredPathSegments
        self._createDependencyGraph()
        
    def _createDependencyGraph(self):
        bundleNames = [bundle.name for bundle in self.bundles]
        numDependencies = [bundle.numberOfDependencies for bundle in self.bundles]
        numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
        for bundle in self.bundles:
            ignored = any(ignoredSegment in bundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored:
                nodeSize = self._interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
                self.addNode(bundle.name, width=str(nodeSize), height=str(nodeSize))
                for reqBundle in bundle.requiredBundles:
                    ignored = any(ignoredSegment in reqBundle for ignoredSegment in self.ignoredPathSegments)
                    if not ignored:
                        if reqBundle in bundleNames: 
                            nodeSize = self._interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                            self.addNode(reqBundle, width=str(nodeSize), height=str(nodeSize))
                        elif self.addNode(reqBundle, color=self._WHITE): 
                            print ("Bundle %s is not contained in workspace." % reqBundle)
                        self._graph.addEdge(bundle.name, reqBundle, label="requires")
                for importedPackage in bundle.importedPackages:
                    self._addEdgeForPackageImport(bundle.name, importedPackage, self.bundlesForExports, numDependenciesForBundle)

    def _interpolateLinear(self, numDependencies, maxNumDependencies):
        divisor = maxNumDependencies if maxNumDependencies > 0 else 1
        result = (numDependencies / divisor) * (self._MAX_NODE_SIZE - self._MIN_NODE_SIZE) + self._MIN_NODE_SIZE
        return round(result,0)

    def _addEdgeForPackageImport(self, sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                nodeSize = self._interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
                self.addNode(exportingBundle.name, width=str(nodeSize), height=str(nodeSize))
                self._graph.addEdge(sourceBundle, exportingBundle.name, label="imports "+importedPackage)
        else:
            ignored = any(ignoredSegment in importedPackage for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                if self.addNode(importedPackage, color=self._WHITE, shape="rectangle"):
                    print ("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
                self._graph.addEdge(sourceBundle, importedPackage, label="imports")
