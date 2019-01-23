#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import comp.repo.typerepo as repo
import report.plot as plot
import report.xls as xls
from app.analyser import Analyser
from comp.domain import Method, Type


class MethodComp(Analyser):

    @staticmethod
    def name():
        return "methods"

    def load_data(self, workingdir, ignored_path_segments):
        self._types = repo.types(workingdir, ignored_path_segments)

    def analyse(self, ignoredPathSegments):
        self._logger.info("Analysing Method Complexity.")
        data = []
        for type_ in self._types:
            for method in type_.methods:
                complexity = method.complexity
                path = type_.path
                data.append((method.name, complexity,  path))
        complexity_col = "Complexity"
        df = pd.DataFrame(data, columns=["Method", complexity_col, "Path"])
        self._df = df.sort_values(complexity_col, ascending=False)
        return self._df

    def write_results(self, outputdir):
        xls.write_data_frame(
            self._df, "cognitive_complexity_per_method.xls",
            outputdir, "Method Complexity")
        methods_with_comp_greater_null = self._create_barchart_data()
        plot.plot_barchart(methods_with_comp_greater_null, "Cognitive complexity",
                           "Methods with highest cognitive complexity",
                           outputdir, "most_complex_methods.pdf")

    def _create_barchart_data(self):
        methods_with_comp = self._df.drop(columns=["Path"])
        return methods_with_comp[methods_with_comp.Complexity > 0]
