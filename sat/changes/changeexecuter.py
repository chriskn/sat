#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sat.changes.analyser.filechanges import FileChanges
from sat.changes.analyser.packagechanges import PackageChanges
from sat.changes.analyser.projectchanges import ProjectChanges

from sat.app.execution.executer import Executer, ExecuterArgs, Option

from sat.changes.changeworkspace import ChangeWorkspace

_ANALYSERS = [FileChanges, PackageChanges, ProjectChanges]


class ChangeExecuter(Executer):
    def __init__(self, directory, ignored_path_segments, output_dir, since):
        workspace = ChangeWorkspace(directory, ignored_path_segments, since)
        Executer.__init__(self, _ANALYSERS, workspace, output_dir)

    @staticmethod
    def args():
        return ExecuterArgs(
            "changes",
            [analyser_class.name() for analyser_class in _ANALYSERS],
            "Git changes analysers",
            [
                Option(
                    "-s",
                    "since",
                    "Date since when the changes were made in ISO 8601. Examples: 2009-06-30, 2009-06-30T18:30:00",
                )
            ],
        )
