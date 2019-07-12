#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import sat.app.report.plot as plot
import sat.app.report.writer as writer

from sat.app.execution.analyser import Analyser


class MethodComp(Analyser):
    @staticmethod
    def name():
        return "methods"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._types = []
        self._analysis_result = None

    def load_data(self):
        for sfile in self._workspace.sourcefiles():
            self._types.extend(sfile.types)

    def analyse(self):
        self._logger.info("Analysing Method Complexity.")
        data = []
        for type_ in self._types:
            for method in type_.methods:
                complexity = method.complexity
                path = type_.path
                data.append((method.name, complexity, path))
        complexity_col = "Complexity"
        method_dataframe = pd.DataFrame(
            data, columns=["Method", complexity_col, "Path"]
        )
        self._analysis_result = method_dataframe.sort_values(
            complexity_col, ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "cognitive_complexity_per_method.xls",
            output_dir,
            "Method Complexity",
        )
        methods_with_comp_greater_zero = self._create_barchart_data()
        plot.plot_barchart(
            methods_with_comp_greater_zero,
            "Cognitive complexity",
            "Methods with highest cognitive complexity",
            output_dir,
            "most_complex_methods.pdf",
        )

    def _create_barchart_data(self):
        methods_with_comp = self._analysis_result.drop(columns=["Path"])
        return methods_with_comp[methods_with_comp.Complexity > 0]
