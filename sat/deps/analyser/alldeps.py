#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sat.app.execution.analyser import Analyser
from sat.deps.analyser.bundledeps import BundleDepsAnalyser
from sat.deps.analyser.packagedeps import PackageDepsAnalyser
from sat.deps.analyser.projectdeps import ProjectDepsAnalyser


class AllDepsAnalyser(Analyser):
    # pylint: disable=R0902
    @staticmethod
    def name():
        return "all"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._bundle_analyser = BundleDepsAnalyser(workspace)
        self._project_analyser = ProjectDepsAnalyser(workspace)
        self._package_analyser = PackageDepsAnalyser(workspace)

    def load_data(self):
        self._bundle_analyser.load_data()
        self._project_analyser.load_data()
        self._package_analyser.load_data()

    def analyse(self):
        self._bundle_analyser.analyse()
        self._project_analyser.analyse()
        self._package_analyser.analyse()

    def write_results(self, output_dir):
        self._bundle_analyser.write_results(output_dir)
        self._project_analyser.write_results(output_dir)
        self._package_analyser.write_results(output_dir)
