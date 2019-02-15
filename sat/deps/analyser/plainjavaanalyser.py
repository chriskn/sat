#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import numpy as np
import pandas as pd

import report.plot as plot
from app.analyser import Analyser
from deps.graph.packagegraph import PackageGraph
from deps.graph.projectgraph import ProjectGraph
import deps.parser.projectparser as parser
from deps.graph.classdiagramm import ClassDiagramm

_CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')
_LIST_SEPARATOR = ", "


class PlainJavaAnalyser(Analyser):

    @staticmethod
    def name():
        return "javaDeps"

    def load_data(self, workingDir, ignoredPathSegments):
        self._logger.info("Loading project data...")
        projects = parser.parse(workingDir, ignoredPathSegments)
        self._projects = projects
        self._packages = []
        for p in self._projects:
            self._packages.extend(p.source_packages)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Creating project dependency graph")
        self._projectGraph = ProjectGraph(self._projects)
        self._logger.info("Analysing project cycles")
        self._project_cycles = self._projectGraph.cycles()
        self._projectGraph.mark_cycles(self._project_cycles)
        self._cycle_project_graph = self._projectGraph.cycle_graph(
            self._project_cycles)
        self._logger.info("Creating project coupling map")
        self._logger.info("Analysed %d projects" % len(self._projects))
        self._project_coupling_map = self._project_coupling_data_frame(
            self._projects)

        self._logger.info("Creating package dependency graph")
        self._package_graph = PackageGraph(self._packages)
        self._logger.info("Analysing package cycles")
        self._package_cycles = self._package_graph.cycles()
        self._package_graph.mark_cycles(self._package_cycles)
        self._cycle_package_graph = self._package_graph.cycle_graph(
            self._package_cycles)
        self._logger.info("Creating package coupling map")
        self._packageCouplingMap = self._createPackageCouplingDataFrame(
            self._packages)
        self._logger.info("Analysed %d packages" % len(self._packages))
        self._logger.info("Creating class diagramm")
        self._class_diagramm = ClassDiagramm(self._packages)
        self._class_clycles = self._class_diagramm.cycles(grouped=True)
        self._class_diagramm.mark_cycles(self._class_clycles, grouped=True)
        self._cycle_class_diagramm = self._class_diagramm.cycle_graph(self._class_clycles)

    def write_results(self, output_dir):
        self._logger.info("Writing project analysis results")
        self._write_graphml(os.path.join(
            output_dir, "project_dependencies.graphml"), self._projectGraph)
        self._write_graphml(
            os.path.join(
                output_dir,
                "cyclic_project_dependencies.graphml"),
            self._cycle_project_graph)
        self._write_cycles_to_txt(os.path.join(
            output_dir, "project_cycles.txt"), self._project_cycles)
        plot.plot_heatmap(self._project_coupling_map, "Project Coupling",
                          output_dir, "project_coupling_heatmap.pdf")

        self._logger.info("Writing package analysis results")
        self._write_cycles_to_txt(os.path.join(
            output_dir, "package_cycles.txt"), self._package_cycles)
        self._write_graphml(os.path.join(
            output_dir, "package_dependencies.graphml"), self._package_graph)
        self._write_graphml(
            os.path.join(
                output_dir,
                "cyclic_package_dependencies.graphml"),
            self._cycle_package_graph)
        plot.plot_heatmap(self._packageCouplingMap, "Package Coupling",
                          output_dir, "package_coupling_heatmap.pdf")
        # Classes
        self._write_graphml(
            os.path.join(output_dir, "classdiagramm.graphml"),
            self._class_diagramm)
        self._write_cycles_to_txt(os.path.join(
            output_dir, "class_cycles.txt"), self._class_clycles)
        self._cycle_class_diagramm = self._write_graphml(
            os.path.join(
                output_dir,
                "cyclic_classes.graphml"),
            self._cycle_class_diagramm)

    def _project_coupling_data_frame(self, projects):
        proj_names = []
        data = []
        for project in reversed(projects):
            proj_imports = [self._to_package_import(
                imp) for imp in project.imports()]
            proj_names.append(project.name)
            proj_data = []
            for other_project in projects:
                proj_deps = 0
                for other_package in other_project.source_packages:
                    occurences = proj_imports.count(other_package.name)
                    proj_deps += occurences
                proj_data.append(proj_deps)
            data.append(proj_data)
        return pd.DataFrame(
            data=data,
            index=proj_names,
            columns=list(
                reversed(proj_names)))

    def _write_graphml(self, path, graph):
        with open(path, 'w') as output_file:
            output_file.write(graph.serialize())

    def _write_cycles_to_txt(self, path, cycles):
        with open(path, 'w') as output_file:
            for cycle in cycles:
                cycle_list = _LIST_SEPARATOR.join(sorted(cycle))
                output_file.write(cycle_list + "\n")

    def _to_package_import(self, import_):
        if _CLASS_IMPORT_PATTERN.match(import_):
            return re.split(r'\.[A-Z]', import_, maxsplit=1)[0]
        else:
            return import_

    def _createPackageCouplingDataFrame(self, packages):
        names = [p.name for p in packages]
        data = []
        for package in reversed(packages):
            package_imps = [self._to_package_import(
                imp) for imp in package.imports()]
            data.append([package_imps.count(pName) for pName in names])
        df = pd.DataFrame(
            data=data,
            index=list(
                reversed(names)),
            columns=names)
        return df
