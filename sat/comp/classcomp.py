#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

import comp.typerepo as repo
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
        pass

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self._write_barchart(outputdir)

    def _write_report(self, outputdir):
        rows = []
        head = ["Class", "Cognitive Complexity",
                "Methods with complexity > 0", "Path"]
        for type_ in self._types:
            methods = ["%s:%d" % (method.name, method.complexity) for method in sorted(type_.methods,
                key=lambda x:x.complexity, reverse=True) if method.complexity > 0]
            rows.append([type_.name, type_.complexity(),
                         ", ".join(methods), type_.path])
        rows.sort(key=lambda x: x[1], reverse=True)
        rows.insert(0, head)
        filepath = os.path.join(
            outputdir, "cognitive_complexity_per_class.xls")
        sheet_name = "Class Complexity"
        xls.write_xls(sheet_name, rows, filepath)

    def _write_barchart(self, outputDir):
        data = []
        for type_ in self._types:
            complexity = type_.complexity()
            if complexity > 0:
                data.append((type_.name, complexity))
        data.sort(key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(data, columns=["Class", "Complexity"])
        if not df.empty:
            plot.plot_barchart(df, "Cognitive complexity",
                               "Classes with highest cognitive complexity", outputDir, "most_complex_classes.pdf")
