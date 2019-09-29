#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.deps.coupling as coupling
import sat.app.report.plot as plot
import sat.app.report.writer as writer
from sat.app.execution.analyser import Analyser
from sat.deps.graph.classdiagramm import ClassDiagramm
from sat.deps.graph.packagegraph import PackageGraph


class PackageDepsAnalyser(Analyser):
    # pylint: disable=R0902
    @staticmethod
    def name():
        return "packages"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._packages = []
        self._package_graph = None
        self._package_cycles = []
        self._cycle_package_graph = None
        self._package_coupling_data_frame = None
        self._number_of_abstract_classes = None
        self._number_of_concrete_classes = None
        self._class_diagramm = None
        self._class_clycles = []
        self._cycle_class_diagramm = None

    def load_data(self):
        self._logger.info("Loading package data...")
        self._packages = self._workspace.packages()

    def analyse(self):
        self.graph_analysis()
        self._package_coupling_data_frame = coupling.package_coupling_dataframe(
            self._packages
        )
        data = []
        for package in self._packages:
            blub = coupling.num_packages_importing_package(self._packages, package)
            blub1 = coupling.num_packages_imported_by_package(package)
            data.append(
                (
                    package.abs_path,
                    package.name,
                    package.num_concrete_classes,
                    package.num_abstract_classes,
                )
            )
        self._logger.info("Analysed %d packages", len(self._packages))

    def graph_analysis(self):
        self._logger.info("Creating package dependency graph")
        self._package_graph = PackageGraph(self._packages)
        self._logger.info("Analysing package cycles")
        self._package_cycles = self._package_graph.cycles()
        self._package_graph.mark_cycles(self._package_cycles)
        self._cycle_package_graph = self._package_graph.cycle_graph(
            self._package_cycles
        )
        self._logger.info("Creating class diagramm")
        self._class_diagramm = ClassDiagramm(self._packages)
        self._class_clycles = self._class_diagramm.cycles(grouped=True)
        self._class_diagramm.mark_cycles(self._class_clycles, grouped=True)
        self._cycle_class_diagramm = self._class_diagramm.cycle_graph(
            self._class_clycles
        )

    def write_results(self, output_dir):
        self._logger.info("Writing package analysis results")
        writer.write_cycles_to_txt(
            os.path.join(output_dir, "package_cycles.txt"), self._package_cycles
        )
        writer.write_graphml(
            os.path.join(output_dir, "package_dependencies.graphml"),
            self._package_graph,
        )
        writer.write_graphml(
            os.path.join(output_dir, "cyclic_package_dependencies.graphml"),
            self._cycle_package_graph,
        )
        plot.plot_heatmap(
            self._package_coupling_data_frame,
            "Package Coupling",
            output_dir,
            "package_coupling_heatmap.pdf",
        )
        writer.write_graphml(
            os.path.join(output_dir, "classdiagramm.graphml"), self._class_diagramm
        )
        writer.write_cycles_to_txt(
            os.path.join(output_dir, "class_cycles.txt"), self._class_clycles
        )
        writer.write_graphml(
            os.path.join(output_dir, "cyclic_classes.graphml"),
            self._cycle_class_diagramm,
        )
