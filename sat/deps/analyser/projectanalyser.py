#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import numpy as np
import pandas as pd

import report.plot as plot
from app.analyser import Analyser
from deps.graph.projectgraph import ProjectGraph
import deps.parser.projectparser as parser


class ProjectAnalyser(Analyser):

    @staticmethod
    def name():
        return "javaProjectDeps"

    def load_data(self, workingDir, ignoredPathSegments):
        self._logger.info("Loading project data...")
        self._projects = parser.parse(workingDir, ignoredPathSegments)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Creating project coupling graph")
        project_graph = ProjectGraph(self._projects)
        self._logger.info("Analysing project cycles")
        cycles = project_graph.cycles()
        project_graph.mark_cycles(cycles)
        self._projectGraph = project_graph
        self._cycleProjectGraph = project_graph.cycle_graph(cycles)
        self._logger.info("Creating project coupling map")
        self._projectCouplingMap = self._create_project_coupling_data_frame(
            self._projects)
        self._logger.info("Analysed %d projects" % len(self._projects))

    def write_results(self, outputDir):
        self._logger.info("Writing project analysis results")
        plot.plot_heatmap(self._project_coupling_map, "Project Coupling",
                          outputDir, "project_coupling_heatmap.pdf")
        self._write_to_graphMl(os.path.join(
            outputDir, "project_dependencies.graphml"), self._projectGraph)
        self._write_to_graphMl(
            os.path.join(
                outputDir,
                "cyclic_project_dependencies.graphml"),
            self._cycle_project_graph)

    def _create_project_coupling_data_frame(self, projects):
        proj_name = []
        data = []
        for project in reversed(projects):
            proj_imports = project.imports
            proj_name.append(project.name)
            proj_data = []
            for o_project in projects:
                proj_deps = 0
                for other_package in o_project.source_packages:
                    occurences = proj_imports.count(other_package.name)
                    proj_deps += occurences
                proj_data.append(proj_deps)
            data.append(proj_data)
        return pd.DataFrame(
            data=data,
            index=proj_name,
            columns=list(
                reversed(proj_name)))

    def _write_to_graphMl(self, path, graph):
        with open(path, 'w') as output_file:
            output_file.write(graph.serialize())
