#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import sat.comp.repo.projectrepo as prepo

import sat.report.plot as plot
import sat.report.writer as writer

from sat.app.analyser import Analyser

_COLUMNS = ["Project", "Complexity", "Path"]


class ProjectComp(Analyser):
    @staticmethod
    def name():
        return "projects"

    def __init__(self):
        self._projects = None
        self._analysis_result = None

    def load_data(self, working_dir, ignored_path_segments):
        self._projects = prepo.projects(working_dir, ignored_path_segments)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing Project Complexity.")
        data = []
        for project in self._projects:
            data.append((project.name, project.complexity, project.path))
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
        tm_data = self._create_treemap_data()
        plot.plot_treemap(
            tm_data,
            "Cognitive complexity per project",
            output_dir,
            "cognitive_complexity_per_project.pdf",
            "complexity:",
        )

    def _create_treemap_data(self):
        tm_data = self._analysis_result.drop(columns=["Path"])
        return tm_data[tm_data.Complexity > 0]
