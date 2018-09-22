#!/usr/bin/env python
# -*- coding: utf-8 -*-

from domain import Bundle
from graph import Graph
import logging

class BundleGraph(Graph):
    
    _WHITE = "#FFFFFF"
    
    def __init__(self, bundles, bundlesForExports, ignoredPathSegments):
        Graph.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.bundles = bundles
        self.bundlesForExports = bundlesForExports
        self.ignoredPathSegments = ignoredPathSegments
        self._createDependencyGraph()
        
    def _createDependencyGraph(self):
        bundleNames = [bundle.name for bundle in self.bundles]
        numDependencies = [bundle.numberOfDependencies for bundle in self.bundles]
        numDependenciesForBundle = dict(zip(bundleNames, numDependencies))
        for bundle in self.bundles:
            nodeSize = self.interpolateLinear(bundle.numberOfDependencies, max(numDependencies))
            self.addNode(bundle.name, width=nodeSize, height=nodeSize)
            for reqBundle in bundle.requiredBundles:
                ignored = any(ignoredSegment in reqBundle for ignoredSegment in self.ignoredPathSegments)
                if not ignored:
                    if reqBundle in bundleNames: 
                        nodeSize = self.interpolateLinear(numDependenciesForBundle[reqBundle], max(numDependencies))
                        self.addNode(reqBundle, width=nodeSize, height=nodeSize)
                    elif self.addNode(reqBundle, color=self._WHITE): 
                        self.logger.info("Bundle %s is not contained in workspace." % reqBundle)
                    self.addEdge(bundle.name, reqBundle, label="requires")
                for importedPackage in bundle.importedPackages:
                    self._addEdgeForPackageImport(bundle.name, importedPackage, self.bundlesForExports, numDependenciesForBundle)

    def _addEdgeForPackageImport(self, sourceBundle, importedPackage, bundlesForExports, numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(ignoredSegment in exportingBundle.path for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                nodeSize = self.interpolateLinear(numDependenciesForBundle[exportingBundle.name], max(list(numDependenciesForBundle.values())))
                self.addNode(exportingBundle.name, width=nodeSize, height=nodeSize)
                self.addEdge(sourceBundle, exportingBundle.name, label="imports "+importedPackage)
        else:
            ignored = any(ignoredSegment in importedPackage for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                if self.addNode(importedPackage, color=self._WHITE, shape="rectangle"):
                    self.logger.info("Exporting bundle not found for import %s. Created package node instead"% importedPackage)
                self.addEdge(sourceBundle, importedPackage, label="imports")
