#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re

import pandas as pd

import changes.changerepo as repo
import report.plot as plot
import report.xls as xls
import scanner
from app.analyser import Analyser


class ProjectChanges(Analyser):

    _COLUMNS = ["Path", "Project", "Total changes", "Lines added", "Lines Removed"]

    @staticmethod
    def name():
        return "projects"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_project = []
        self._working_dir = None
        self._project_paths = None
        self._analysis_result = None

    def load_data(self, working_dir, ignored_path_segments):
        self._working_dir = working_dir
        self._changes = repo.changes(working_dir, self._since)
        self._project_paths = scanner.find_projects(
            self._working_dir, ignored_path_segments
        )

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing project changes.")
        data = []
        for project_path, proj_name in self._project_paths.items():
            rel_proj_path, lines_added, lines_removed = self._count_changed_lines(
                project_path
            )
            data.append(
                (
                    rel_proj_path,
                    proj_name,
                    lines_added + lines_removed,
                    lines_added,
                    lines_removed,
                )
            )
        dataframe = pd.DataFrame(data=data, columns=ProjectChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(
            ProjectChanges._COLUMNS[2], ascending=False
        )
        return self._analysis_result

    def _count_changed_lines(self, project_path):
        lines_added = 0
        lines_removed = 0
        rel_proj_path = None
        for change in self._changes:
            change_directory = os.path.normpath(os.path.dirname(change.path))
            rel_proj_path = self._norm_path(project_path)
            if rel_proj_path in change_directory:
                lines_added += change.lines_added
                lines_removed += change.lines_removed
        return rel_proj_path, lines_added, lines_removed

    def _norm_path(self, full_project_path):
        norm_package_path = full_project_path.replace(self._working_dir, "")
        rel_pattern = "^[.]*" + re.escape(os.sep)
        if re.match(rel_pattern, norm_package_path):
            norm_package_path = re.sub(rel_pattern, "", norm_package_path)
        return norm_package_path

    def write_results(self, output_dir):
        xls.write_data_frame(
            self._analysis_result,
            "changed_lines_per_project.xls",
            output_dir,
            "Changes since " + self._since,
        )
        tm_data = self._create_tm_data()
        plot.plot_treemap(
            tm_data,
            "Number of changed lines per project since " + self._since,
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
