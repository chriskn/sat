#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xls
from analysis.analysis import Analysis
from comp.domain import Method
from comp.domain import Type
import comp.typerepo as repo
import plot
import pandas as pd

class MethodComp(Analysis):

    @staticmethod
    def name():
        return "methods"

    def load_data(self, workingdir, ignored_path_segments):
        self._types = repo.types(workingdir, ignored_path_segments)

    def analyse(self, ignoredPathSegments):
        pass

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self._write_barchart(outputdir)

    def _write_report(self, outputdir):
        rows = []
        head = ["Method", "Cognitive Complexity", "Path"]
        for type_ in self._types:
            for method in type_.methods:
                rows.append([method.name, method.complexity, type_.path])
        rows.sort(key=lambda x: x[1], reverse=True)
        rows.insert(0,head)
        filepath = os.path.join(
            outputdir, "cognitive_complexity_per_method.xls")
        sheet_name = "Method Complexity"
        xls.write_xls(sheet_name, rows, filepath)

    def _write_barchart(self, outputDir):
        data = []
        for type_ in self._types:
            for method in type_.methods:
                data.append((method.name, method.complexity))
        data.sort(key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(data, columns=["Method", "Complexity"])
        if not df.empty:
            plot.plot_barchart(df, "Cognitive complexity",
                                       "Methods with highest cognitive complexity", outputDir, "most_complex_methods.pdf")
