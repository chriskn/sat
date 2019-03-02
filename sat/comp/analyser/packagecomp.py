#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

import comp.repo.packagerepo as prepo

import report.plot as plot
import report.xls as xls

from app.analyser import Analyser

_COLUMNS = ["Package", "Complexity", "Average complexity by class", "Average complexity by method", "Path"]


class PackageComp(Analyser):

    @staticmethod
    def name():
        return "packages"

    def __init__(self):
        self._packages = None
        self._analysis_result = None

    def load_data(self, working_dir, ignored_path_segments):
        self._packages = prepo.packages(working_dir, ignored_path_segments)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing Package Complexity.")
        data = []
        for package in self._packages:
            num_types = len(package.types)
            num_methods = sum([len(type_.methods) for type_ in package.types])
            av_method_comp = 0
            av_type_comp = 0
            if num_methods > 0:
                av_method_comp = package.complexity / num_methods
            if num_types > 0:
                av_type_comp = package.complexity / num_types
            data.append((package.name, package.complexity, av_type_comp, av_method_comp, package.path))
        package_dataframe = pd.DataFrame(data, columns=_COLUMNS)
        self._analysis_result = package_dataframe.sort_values(_COLUMNS[1], ascending=False)
        return self._analysis_result

    # def _count_methods(self, package):
    #     num_methods = 0
    #     [num_methods += len(type_.methods) for type_ in package.types]
    #     for type_ in package.types:
    #         num_methods += len(type_.methods)
    #     return num_methods

    def write_results(self, output_dir):
        xls.write_data_frame(self._analysis_result, "cognitive_complexity_per_package.xls",
                             output_dir, "Package Complexity")
        self._plot_treemaps(output_dir)

    def _plot_treemaps(self, output_dir):
        total_comp = self._create_treemap_data(_COLUMNS[1])
        avm_comp = self._create_treemap_data(_COLUMNS[2])
        avt_comp = self._create_treemap_data(_COLUMNS[3])
        plot.plot_treemap(total_comp, "Cognitive complexity per package",
                          output_dir, "cognitive_complexity_per_package.pdf", "complexity:")
        plot.plot_treemap(avm_comp, "av method complexity per package",
                          output_dir, "av_method_complexity_per_package.pdf", "avm complexity:")
        plot.plot_treemap(avt_comp, "av class complexity per package",
                          output_dir, "av_class_complexity_per_package.pdf", "avc complexity:")

    def _create_treemap_data(self, data_column):
        columns_to_drop = list(_COLUMNS)
        columns_to_drop.remove(data_column)
        columns_to_drop.remove(_COLUMNS[0])
        tm_data = self._analysis_result.drop(columns=columns_to_drop)
        return tm_data[tm_data[data_column] > 0]
