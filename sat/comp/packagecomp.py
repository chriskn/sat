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

class PackageComp(Analysis):

    @staticmethod
    def name():
        return "packages"

    def load_data(self, workingdir, ignored_path_segments):
        self._types = repo.types(workingdir, ignored_path_segments)
        self._comp_by_package = dict()
        self._relativepaths_for_package_paths = scanner.find_packages(
            workingdir, ignored_path_segments)

    def analyse(self, ignoredPathSegments):
        if not self._relativepaths_for_package_paths:
            self._logger.warn("No packages found. No output will be written.")
            return
        for package_path in self._relativepaths_for_package_paths:
            package_comp = 0
            for type_ in self._types:
                type_directory = os.path.normpath(
                    os.path.dirname(type_.path))
                if type_directory.endswith(package_path):
                    package_comp += type_.complexity()
            self._comp_by_package[package_path] = package_comp

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self._write_treemap(outputdir)

    def _write_report(self, outputdir):
        rows = []
        head = ["Package", "Cognitive Complexity", "Path"]
        for package_path, comp in self._comp_by_package.items():
            package_name = self._relativepaths_for_package_paths.get(
                package_path).replace("\\", ".")
            rows.append([package_name, comp, package_path])
        rows.sort(key=lambda x: x[1], reverse=True)
        rows.insert(0, head)
        filepath = os.path.join(
            outputdir, "cognitive_complexity_per_package.xls")
        sheet_name = "Package Complexity"
        xls.write_xls(sheet_name, rows, filepath)


    def _write_treemap(self, outputdir):
        data = OrderedDict()
        for package_path, complexity in self._comp_by_package.items():
            package_name = self._relativepaths_for_package_paths.get(
                package_path).replace("\\", ".")
            if complexity > 0: 
                data[package_name] = int(complexity)
        if data:
            plot.plot_treemap(data, "Cognitive complexity per package", outputdir, "cognitive_complexity_per_package.pdf", "complexity:")

