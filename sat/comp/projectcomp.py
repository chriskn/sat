#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

import comp.typerepo as repo
import plot
import xls
from analysis.analysis import Analysis
from comp.domain import Method, Type
import scanner
from collections import OrderedDict

class ProjectComp(Analysis):

    @staticmethod
    def name():
        return "projects"

    def load_data(self, workingdir, ignored_path_segments):
        self._types = repo.types(workingdir, ignored_path_segments)
        self._comp_by_project = dict()
        self._project_paths = scanner.find_projects(
            workingdir, ignored_path_segments)
        self._workingdir = workingdir

    def analyse(self, ignoredPathSegments):
        if not self._project_paths:
            self._logger.warn("No projects found. No output will be written.")
            return
        for project_path in self._project_paths:
            project_comp = 0
            for type_ in self._types:
                type_directory = os.path.normpath(
                    os.path.dirname(type_.path))
                rel_proj_path =  project_path.replace(self._workingdir, "")
                if rel_proj_path.startswith("\\"):
                    rel_proj_path = rel_proj_path[1:]
                if rel_proj_path in type_directory:
                    project_comp += type_.complexity()
            self._comp_by_project[project_path] = project_comp

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self._write_treemap(outputdir)

    def _write_report(self, outputdir):
        rows = []
        head = ["Project", "Cognitive Complexity", "Path"]
        for project_path, comp in self._comp_by_project.items():
            project_name = os.path.basename(project_path)
            rows.append([project_name, comp, project_path])
        rows.sort(key=lambda x: x[1], reverse=True)
        rows.insert(0, head)
        filepath = os.path.join(
            outputdir, "cognitive_complexity_per_project.xls")
        sheet_name = "Project Complexity"
        xls.write_xls(sheet_name, rows, filepath)

    def _write_treemap(self, outputdir):
        data = OrderedDict()
        for project_path, comp in self._comp_by_project.items():
            project_name = os.path.basename(project_path)
            if comp > 0: 
                data[project_name] = int(comp)
        if data:
            plot.plot_treemap(data, "Cognitive complexity per package", outputdir, "cognitive_complexity_per_project.pdf", "complexity:")

