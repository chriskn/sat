#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import sat.app.report.plot as plot
import sat.app.report.writer as writer

from sat.app.execution.analyser import Analyser

_COLUMNS = ["Project", "Complexity", "Path"]


class ProjectComp(Analyser):
    @staticmethod
    def name():
        return "projects"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._projects = None
        self._analysis_result = None

    def load_data(self):
        self._projects = self._workspace.projects()

    def analyse(self):
        self._logger.info("Analysing Project Complexity.")
        data = []
        for project in self._projects:
            data.append((project.name, project.complexity, project.abs_path))
        project_data = pd.DataFrame(data, columns=_COLUMNS)
        self._analysis_result = project_data.sort_values(_COLUMNS[1], ascending=False)
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "cognitive_complexity_per_project.xls",
            output_dir,
            "Project Complexity",
        )
        tm_data = self._analysis_result.drop(columns=["Path"])
        tm_data = tm_data[tm_data["Complexity"] > 0]

        plot.plot_treemap(
            tm_data,
            "Cognitive complexity per project",
            output_dir,
            "cognitive_complexity_per_project.pdf",
            "complexity:",
        )
