#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
from project.projectgraph import ProjectGraph
from package.packagegraph import PackageGraph
from analysis.analysis import Analysis
import numpy as np
import pandas as pd
import os
import plot
import re
from package.classdiagramm import ClassDiagramm

_CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')
_LIST_SEPARATOR = ", "


class PlainJavaAnalyser(Analysis):

    @staticmethod
    def name():
        return "javaDeps"

    def load_data(self, workingDir, ignoredPathSegments):
        self._logger.info("Loading project data...")
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parse()
        self._projects = projects
        self._packages = []
        for p in self._projects:
            self._packages.extend(p.source_packages)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Creating project dependency graph")
        self._projectGraph = ProjectGraph(self._projects)
        self._logger.info("Analysing project cycles")
        self._projectCycles = self._projectGraph.cycles()
        self._projectGraph.mark_cycles(self._projectCycles)
        self._cycleProjectGraph = self._projectGraph.cycle_graph(
            self._projectCycles)
        self._logger.info("Creating project coupling map")
        self._logger.info("Analysed %d projects" % len(self._projects))
        self._projectCouplingMap = self._project_coupling_data_frame(
            self._projects)

        self._logger.info("Creating package dependency graph")
        self._packageGraph = PackageGraph(self._packages)
        self._logger.info("Analysing package cycles")
        self._packageCycles = self._packageGraph.cycles()
        self._packageGraph.mark_cycles(self._packageCycles)
        self._cyclePackageGraph = self._packageGraph.cycle_graph(
            self._packageCycles)
        self._logger.info("Creating package coupling map")
        self._packageCouplingMap = self._createPackageCouplingDataFrame(
            self._packages)
        self._logger.info("Creating class diagramm")
        self._classDiagramm = ClassDiagramm(self._packages)
        self._logger.info("Analysed %d packages" % len(self._packages))

    def write_results(self, outputDir):
        self._logger.info("Writing project analysis results")
        self._write_graphml(os.path.join(
            outputDir, "project_dependencies.graphml"), self._projectGraph)
        self._write_graphml(os.path.join(
            outputDir, "cyclic_project_dependencies.graphml"), self._cycleProjectGraph)
        self._write_cycles_to_txt(os.path.join(
            outputDir, "project_cycles.txt"), self._projectCycles)
        plot.plot_heatmap(self._projectCouplingMap, "Project Coupling",
                          outputDir, "project_coupling_heatmap.pdf")
 
        self._logger.info("Writing package analysis results")
        self._write_cycles_to_txt(os.path.join(
            outputDir, "package_cycles.txt"), self._packageCycles)
        self._write_graphml(os.path.join(
            outputDir, "package_dependencies.graphml"), self._packageGraph)
        self._write_graphml(os.path.join(
            outputDir, "cyclic_package_dependencies.graphml"), self._cyclePackageGraph)
        plot.plot_heatmap(self._packageCouplingMap, "Package Coupling",
                          outputDir, "package_coupling_heatmap.pdf")
        self._write_graphml(os.path.join(outputDir, "classdiagramm.graphml"), self._classDiagramm)

    def _project_coupling_data_frame(self, projects):
        proj_names = []
        data = []
        for project in reversed(projects):
            proj_imports = [self._to_package_import(imp) for imp in project.imports()]
            proj_names.append(project.name)
            proj_data = []
            for other_project in projects:
                proj_deps = 0
                for other_package in other_project.source_packages:
                    occurences = proj_imports.count(other_package.name)
                    proj_deps += occurences
                proj_data.append(proj_deps)
            data.append(proj_data)
        return pd.DataFrame(data=data, index=proj_names, columns=list(reversed(proj_names)))

    def _write_graphml(self, path, graph):
        with open(path, 'w') as output_file:
            output_file.write(graph.serialize())

    def _write_cycles_to_txt(self, path, cycles):
        with open(path, 'w') as output_file:
            for cycle in cycles:
                cycle_list = _LIST_SEPARATOR.join(sorted(cycle))
                output_file.write(cycle_list+"\n")
    
    def _to_package_import(self, import_):
        if _CLASS_IMPORT_PATTERN.match(import_):
            return re.split(r'\.[A-Z]', import_, maxsplit=1)[0]
        else:
           return import_

    def _createPackageCouplingDataFrame(self, packages):
        names = [p.name for p in packages]
        data = []
        for package in reversed(packages):
            package_imps = [self._to_package_import(imp) for imp in package.imports()]
            data.append([package_imps.count(pName) for pName in names])
        return pd.DataFrame(data=data, index=list(reversed(names)), columns=names)
