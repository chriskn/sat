#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

import comp.typerepo as repo
import plot
import xls
from analysis.analysis import Analysis
import comp.packagerepo as prepo
import xls

_COLUMNS = ["Package", "Complexity", "Average complexity by class",
                  "Average complexity by method", "Path"]

class PackageComp(Analysis):

    @staticmethod
    def name():
        return "packages"

    def load_data(self, workingdir, ignored_path_segments):
        self._packages = prepo.packages(workingdir, ignored_path_segments)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Analysing Package Complexity.")
        data = []
        for package in self._packages:
            num_types = len(package.types)
            num_methods = self._count_methods(package)
            av_method_comp = 0
            av_type_comp = 0
            if num_methods > 0:
                av_method_comp = package.complexity / num_methods
            if num_types > 0:
                av_type_comp = package.complexity / num_types
            data.append((package.name, package.complexity, av_type_comp, av_method_comp, package.path))
        df = pd.DataFrame(data, columns=_COLUMNS)
        self._df = df.sort_values(_COLUMNS[1], ascending=False)
        return self._df

    def _count_methods(self, package):
        num_methods = 0
        for type_ in package.types:
            num_methods += len(type_.methods)
        return num_methods
            
    def write_results(self, outputdir):
        xls.write_data_frame(self._df, "cognitive_complexity_per_package.xls", outputdir, "Package Complexity")
        self._plot_treemaps(outputdir)

    def _plot_treemaps(self, outputdir):
        total_comp = self._create_treemap_data(_COLUMNS[1])
        avm_comp = self._create_treemap_data(_COLUMNS[2])
        avt_comp = self._create_treemap_data(_COLUMNS[3])
        plot.plot_treemap(total_comp, "Cognitive complexity per package",
                            outputdir, "cognitive_complexity_per_package.pdf", "complexity:")
        plot.plot_treemap(avm_comp, "av method complexity per package",
                            outputdir, "av_method_complexity_per_package.pdf", "avm complexity:")
        plot.plot_treemap(avt_comp, "av class complexity per package",
                            outputdir, "av_class_complexity_per_package.pdf", "avc complexity:")

    def _create_treemap_data(self, data_column):
        columns_to_drop = list(_COLUMNS)
        columns_to_drop.remove(data_column)
        columns_to_drop.remove(_COLUMNS[0])
        tm_data = self._df.drop(columns=columns_to_drop)
        return tm_data[tm_data[data_column] > 0]
