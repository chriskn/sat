#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sat.comp.analyser.classcomp import ClassComp
from sat.comp.analyser.methodcomp import MethodComp
from sat.comp.analyser.packagecomp import PackageComp
from sat.comp.analyser.projectcomp import ProjectComp
from sat.app.execution.executer import Executer, ExecuterArgs
from sat.comp.compworkspace import CompWorkspace

_ANALYSERS = [MethodComp, ClassComp, PackageComp, ProjectComp]


class CompExecuter(Executer):
    def __init__(self, directory, ignored_path_segments, output_dir):
        workspace = CompWorkspace(directory, ignored_path_segments)
        Executer.__init__(self, _ANALYSERS, workspace, output_dir)

    @staticmethod
    def args():
        return ExecuterArgs(
            "comp",
            [analyser_class.name() for analyser_class in _ANALYSERS],
            "Complexity analysers",
        )
