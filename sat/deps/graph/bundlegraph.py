#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deps.domain import Bundle
from deps.graph.graph import Graph
import logging


class BundleGraph(Graph):

    _WHITE = "#FFFFFF"

    def __init__(self, bundles, bundlesForExports, ignoredPathSegments):
        Graph.__init__(self)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._bundles = bundles
        self._bundles_for_exports = bundlesForExports
        self._ignored_path_segments = ignoredPathSegments
        self._create_dependency_graph()

    def _create_dependency_graph(self):
        bundle_names = [bundle.name for bundle in self._bundles]
        num_dependencies = [
            bundle.num_dependencies for bundle in self._bundles]
        num_dependencies_for_bundle = dict(zip(bundle_names, num_dependencies))
        for bundle in self._bundles:
            node_size = self.interpolate_node_size(
                bundle.num_dependencies, max(num_dependencies))
            self.add_node(bundle.name, width=node_size, height=node_size)
            for req_bundle in bundle.required_bundles:
                ignored = any(
                    ignored_segment in req_bundle for ignored_segment in self._ignored_path_segments)
                if not ignored:
                    if req_bundle in bundle_names:
                        node_size = self.interpolate_node_size(
                            num_dependencies_for_bundle[req_bundle], max(num_dependencies))
                        self.add_node(req_bundle, width=node_size,
                                      height=node_size)
                    elif self.add_node(req_bundle, shape_fill=self._WHITE):
                        self._logger.info(
                            "Bundle %s is not contained in workspace." %
                            req_bundle)
                    self.add_edge(bundle.name, req_bundle, label="requires")
                for imported_package in bundle.imported_packages:
                    self._add_edge_for_package_import(
                        bundle.name,
                        imported_package,
                        self._bundles_for_exports,
                        num_dependencies_for_bundle)

    def _add_edge_for_package_import(
            self,
            sourceBundle,
            importedPackage,
            bundlesForExports,
            numDependenciesForBundle):
        if importedPackage in bundlesForExports:
            exportingBundle = bundlesForExports[importedPackage]
            ignored = any(
                ignoredSegment in exportingBundle.path for ignoredSegment in self._ignored_path_segments)
            if not ignored:
                nodeSize = self.interpolate_node_size(numDependenciesForBundle[exportingBundle.name], max(
                    list(numDependenciesForBundle.values())))
                self.add_node(exportingBundle.name,
                              width=nodeSize, height=nodeSize)
                self.add_edge(sourceBundle, exportingBundle.name,
                              label="imports " + importedPackage)
        else:
            ignored = any(
                ignoredSegment in importedPackage for ignoredSegment in self._ignored_path_segments)
            if not ignored:
                if self.add_node(
                        importedPackage,
                        shape_fill=self._WHITE,
                        shape="rectangle"):
                    self._logger.info(
                        "Exporting bundle not found for import %s. Created package node instead" %
                        importedPackage)
                self.add_edge(sourceBundle, importedPackage, label="imports")
