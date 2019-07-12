#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913

from sat.app.workspace.domain import Package as WPackage
from sat.app.workspace.domain import Project as WProject
from sat.app.workspace.domain import SourceFile as WSourcefile


class Project(WProject):
    def __init__(self, abs_path, rel_path, name, packages):
        WProject.__init__(self, abs_path, rel_path, name, packages)
        self.total_lines = sum([package.total_lines for package in packages])
        self.lines_added = sum([package.lines_added for package in packages])
        self.lines_removed = sum([package.lines_removed for package in packages])


class Package(WPackage):
    def __init__(self, abs_path, rel_path, name, sourcefiles):
        WPackage.__init__(self, abs_path, rel_path, name, sourcefiles)
        self.total_lines = sum([sf.change.total_lines for sf in sourcefiles])
        self.lines_added = sum([sf.change.lines_added for sf in sourcefiles])
        self.lines_removed = sum([sf.change.lines_removed for sf in sourcefiles])


class SourceFile(WSourcefile):
    def __init__(self, abs_path, rel_path, name, change, ast=None):
        WSourcefile.__init__(self, abs_path, rel_path, name, ast)
        self.change = change


class Change:
    # pylint: disable=R0903
    def __init__(self, path, lines_added, lines_removed):
        self.path = path
        self.lines_added = int(lines_added)
        self.lines_removed = int(lines_removed)
        self.total_lines = self.lines_added + self.lines_removed
