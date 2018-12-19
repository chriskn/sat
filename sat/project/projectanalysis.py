#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
from project.projectgraph import ProjectGraph
from analysis.analysis import Analysis
import numpy as np
import pandas as pd
import os
import plot
import re


_CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')
_LIST_SEPARATOR = ", "


class ProjectAnalysis(Analysis):

    @staticmethod
    def name():
        return "projectDeps"

    def load_data(self, workingDir, ignoredPathSegments):
        self._logger.info("Loading project data...")
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parse()
        self._projects = projects

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
