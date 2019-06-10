#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from comp.analyser.classcomp import ClassComp
from app.analyser import Analyser

_COLUMNS = [
    "GROUP",
    "PACKAGE",
    "CLASS",
    "INSTRUCTION_MISSED",
    "INSTRUCTION_COVERED",
    "BRANCH_MISSED",
    "BRANCH_COVERED",
    "LINE_MISSED",
    "LINE_COVERED",
    "COMPLEXITY_MISSED",
    "COMPLEXITY_COVERED",
    "METHOD_MISSED",
    "METHOD_COVERED",
]


class ClassCov(Analyser):
    @staticmethod
    def name():
        return "classes"

    def __init__(self, path_to_cov_csv):
        self._analysis_result = None
        self._cov_data = None
        self._path_to_cov_csv = path_to_cov_csv
        self._class_comp_analyser = ClassComp()

    def load_data(self, working_dir, ignored_path_segments):
        self._class_comp_analyser.load_data(working_dir, ignored_path_segments)
        self.read_cov_csv()

    def read_cov_csv(self):
        data = pd.read_csv(self._path_to_cov_csv)
        columns_to_drop = list(_COLUMNS)
        columns_to_drop.remove(_COLUMNS[2])
        columns_to_drop.remove(_COLUMNS[3])
        columns_to_drop.remove(_COLUMNS[4])
        columns_to_drop.remove(_COLUMNS[9])
        self._cov_data = data.drop(columns=columns_to_drop)

    def analyse(self, ignored_path_segments):
        class_comp = self._class_comp_analyser.analyse(ignored_path_segments)

        print(class_comp)

    def write_results(self, output_dir):
        pass
