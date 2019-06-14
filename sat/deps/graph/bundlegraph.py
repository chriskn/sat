#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sat.deps.graph.graph import Graph


class BundleGraph(Graph):

    _WHITE = "#FFFFFF"

    def __init__(self, bundles, bundles_for_exports, ignored_path_segments):
        Graph.__init__(self)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._bundles = bundles
        self._bundles_for_exports = bundles_for_exports
        self._ignored_path_segments = ignored_path_segments
        self._create_dependency_graph()

    def _create_dependency_graph(self):
        bundle_names = [bundle.name for bundle in self._bundles]
        num_dependencies = [bundle.num_dependencies for bundle in self._bundles]
        num_dependencies_for_bundle = dict(zip(bundle_names, num_dependencies))
        for bundle in self._bundles:
            node_size = self.interpolate_node_size(
                bundle.num_dependencies, max(num_dependencies)
            )
            self.add_node(bundle.name, width=node_size, height=node_size)
            for req_bundle in bundle.required_bundles:
                ignored = any(
                    ignored_segment in req_bundle
                    for ignored_segment in self._ignored_path_segments
                )
                if not ignored:
                    if req_bundle in bundle_names:
                        node_size = self.interpolate_node_size(
                            num_dependencies_for_bundle[req_bundle],
                            max(num_dependencies),
                        )
                        self.add_node(req_bundle, width=node_size, height=node_size)
                    elif self.add_node(req_bundle, shape_fill=self._WHITE):
                        self._logger.info(
                            "Bundle %s is not contained in workspace.", req_bundle
                        )
                    self.add_edge(bundle.name, req_bundle, label="requires")
                for imported_package in bundle.imported_packages:
                    self._add_edge_for_package_import(
                        bundle.name,
                        imported_package,
                        self._bundles_for_exports,
                        num_dependencies_for_bundle,
                    )

    def _add_edge_for_package_import(
        self,
        source_bundle,
        imported_package,
        bundles_for_exports,
        num_dependencies_for_bundle,
    ):
        if imported_package in bundles_for_exports:
            exporting_bundle = bundles_for_exports[imported_package]
            ignored = any(
                ignored_segment in exporting_bundle.path
                for ignored_segment in self._ignored_path_segments
            )
            if not ignored:
                node_size = self.interpolate_node_size(
                    num_dependencies_for_bundle[exporting_bundle.name],
                    max(list(num_dependencies_for_bundle.values())),
                )
                self.add_node(exporting_bundle.name, width=node_size, height=node_size)
                self.add_edge(
                    source_bundle,
                    exporting_bundle.name,
                    label="imports " + imported_package,
                )
        else:
            ignored = any(
                ignored_segment in imported_package
                for ignored_segment in self._ignored_path_segments
            )
            if not ignored:
                if self.add_node(
                    imported_package, shape_fill=self._WHITE, shape="rectangle"
                ):
                    self._logger.info(
                        "Exporting bundle not found for import %s. Created package node instead",
                        imported_package,
                    )
                self.add_edge(source_bundle, imported_package, label="imports")
