#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
from collections import OrderedDict

import pandas as pd

import changes.changerepo as repo
import report.plot as plot
import report.xls as xls
import scanner
from app.analyser import Analyser
from changes.domain import Change


class ProjectChanges(Analyser):

    _COLUMNS = ["Path", "Project", "Total changes",
                "Lines added", "Lines Removed"]

    @staticmethod
    def name():
        return "projects"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_project = []

    def load_data(self, workingdir, ignored_path_segments):
        self._workingDir = workingdir
        self._changes = repo.changes(workingdir, self._since)
        self._project_paths = scanner.find_projects(
            self._workingDir, ignored_path_segments)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing project changes.")
        data = []
        for project_path, proj_name in self._project_paths.items():
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                change_directory = os.path.normpath(
                    os.path.dirname(change.path))
                rel_proj_path = self._norm_path(project_path)
                if rel_proj_path in change_directory:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            data.append((rel_proj_path, proj_name, lines_added +
                         lines_removed, lines_added, lines_removed))
        df = pd.DataFrame(data=data, columns=ProjectChanges._COLUMNS)
        self._df = df.sort_values(ProjectChanges._COLUMNS[2], ascending=False)
        return self._df

    def _norm_path(self, full_project_path):
        norm_package_path = full_project_path.replace(self._workingDir, "")
        rel_pattern = "^[.]*"+re.escape(os.sep)
        if re.match(rel_pattern, norm_package_path):
            norm_package_path = re.sub(rel_pattern, '', norm_package_path)
        return norm_package_path

    def write_results(self, outputdir):
        xls.write_data_frame(self._df, "changed_lines_per_project.xls",
                             outputdir, "Changes since "+self._since)
        tm_data = self._create_tm_data()
        plot.plot_treemap(tm_data, "Number of changed lines per project since " +
                          self._since, outputdir, "changed_lines_per_project.pdf", "changes:")

    def _create_tm_data(self):
        tm_data = self._df.drop(columns=[
                                ProjectChanges._COLUMNS[0], ProjectChanges._COLUMNS[3], ProjectChanges._COLUMNS[4]])
        return tm_data[tm_data[ProjectChanges._COLUMNS[2]] > 0]
