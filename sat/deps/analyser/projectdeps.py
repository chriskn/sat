#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.deps.coupling as coupling
import sat.app.report.plot as plot
import sat.app.report.writer as writer
from sat.app.execution.analyser import Analyser
from sat.deps.graph.projectgraph import ProjectGraph


class ProjectDepsAnalyser(Analyser):
    # pylint: disable=R0902
    @staticmethod
    def name():
        return "projects"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._projects = []
        self._project_graph = None
        self._project_cycles = []
        self._cycle_project_graph = None
        self._project_coupling_data_frame = None

    def load_data(self):
        self._logger.info("Loading project data...")
        self._projects = self._workspace.projects()

    def analyse(self):
        self._graph_analysis()
        self._coupling_analysis()

    def _coupling_analysis(self):
        self._logger.info("Creating project coupling map")
        self._logger.info("Analysed %d projects", len(self._projects))
        self._project_coupling_data_frame = coupling.project_coupling_dataframe(
            sorted(self._projects)
        )

    def _graph_analysis(self):
        self._logger.info("Creating project dependency graph")
        self._project_graph = ProjectGraph(self._projects)
        self._logger.info("Analysing project cycles")
        self._project_cycles = self._project_graph.cycles()
        self._project_graph.mark_cycles(self._project_cycles)
        self._cycle_project_graph = self._project_graph.cycle_graph(
            self._project_cycles
        )

    def write_results(self, output_dir):
        self._logger.info("Writing project analysis results")
        writer.write_graphml(
            os.path.join(output_dir, "project_dependencies.graphml"),
            self._project_graph,
        )
        writer.write_graphml(
            os.path.join(output_dir, "cyclic_project_dependencies.graphml"),
            self._cycle_project_graph,
        )
        writer.write_cycles_to_txt(
            os.path.join(output_dir, "project_cycles.txt"), self._project_cycles
        )
        plot.plot_heatmap(
            self._project_coupling_data_frame,
            "Project Coupling",
            output_dir,
            "project_coupling_heatmap.pdf",
        )
