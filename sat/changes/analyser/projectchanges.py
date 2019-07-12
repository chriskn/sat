#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import sat.app.report.plot as plot
import sat.app.report.writer as writer
from sat.app.execution.analyser import Analyser


class ProjectChanges(Analyser):

    _COLUMNS = ["Path", "Project", "Total changes", "Lines added", "Lines Removed"]

    @staticmethod
    def name():
        return "projects"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._projects = []
        self._analysis_result = None

    def load_data(self):
        self._projects = self._workspace.projects()

    def analyse(self):
        self._logger.info("Analysing project changes.")
        data = []
        for project in self._projects:
            data.append(
                (
                    project.abs_path,
                    project.name,
                    project.total_lines,
                    project.lines_added,
                    project.lines_removed,
                )
            )
        dataframe = pd.DataFrame(data=data, columns=ProjectChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(
            ProjectChanges._COLUMNS[2], ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "changed_lines_per_project.xls",
            output_dir,
            "Changes since " + self._workspace.since,
        )
        tm_data = self._create_tm_data()
        plot.plot_treemap(
            tm_data,
            "Number of changed lines per project since " + self._workspace.since,
            output_dir,
            "changed_lines_per_project.pdf",
            "changes:",
        )

    def _create_tm_data(self):
        tm_data = self._analysis_result.drop(
            columns=[
                ProjectChanges._COLUMNS[0],
                ProjectChanges._COLUMNS[3],
                ProjectChanges._COLUMNS[4],
            ]
        )
        return tm_data[tm_data[ProjectChanges._COLUMNS[2]] > 0]
