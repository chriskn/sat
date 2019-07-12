#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sat.deps.analyser.bundledeps import BundleDepsAnalyser
from sat.deps.analyser.alldeps import AllDepsAnalyser
from sat.deps.analyser.packagedeps import PackageDepsAnalyser
from sat.deps.analyser.projectdeps import ProjectDepsAnalyser

from sat.deps.depsworkspace import DepsWorkspace

from sat.app.execution.executer import Executer, ExecuterArgs

_ANALYSERS = [
    AllDepsAnalyser,
    BundleDepsAnalyser,
    ProjectDepsAnalyser,
    PackageDepsAnalyser,
]


class DepsExecuter(Executer):
    def __init__(self, directoy, ignored_path_segments, output_dir):
        workspace = DepsWorkspace(directoy, ignored_path_segments)
        Executer.__init__(self, _ANALYSERS, workspace, output_dir)

    @staticmethod
    def args():
        return ExecuterArgs(
            "deps",
            [analyser_class.name() for analyser_class in _ANALYSERS],
            "Dependency analysers",
        )
