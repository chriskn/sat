#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

import comp.repo.typerepo as repo
import plot
import xls
from analysis.analysis import Analysis
from comp.domain import Method, Type


class ClassComp(Analysis):

    @staticmethod
    def name():
        return "classes"

    def load_data(self, workingdir, ignored_path_segments):
        self._types = repo.types(workingdir, ignored_path_segments)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Analysing Class Complexity.")
        data = []
        complexity_col = "Complexity"
        columns = ["Class", complexity_col,
                   "Methods with complexity > 0", "Path"]
        for type_ in self._types:
            sorted_methods = sorted(
                type_.methods, key=lambda x: x.complexity, reverse=True)
            comp_for_methods = ["%s:%d" % (method.name, method.complexity)
                                for method in sorted_methods
                                if method.complexity > 0]
            data.append([type_.name, type_.complexity,
                         ", ".join(comp_for_methods), type_.path])
        df = pd.DataFrame(data, columns=columns)
        self._df = df.sort_values(complexity_col, ascending=False)
        return self._df

    def write_results(self, outputdir):
        xls.write_data_frame(
            self._df, "cognitive_complexity_per_class.xls", outputdir, "Class Complexity")
        df = self._create_barchart_data()
        plot.plot_barchart(df, "Cognitive complexity",
                               "Classes with highest cognitive complexity", outputdir, "most_complex_classes.pdf")

    def _create_barchart_data(self):
        classes_with_comp = self._df.drop(
            columns=["Methods with complexity > 0", "Path"])
        return classes_with_comp[classes_with_comp.Complexity > 0]
