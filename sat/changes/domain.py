#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913

from sat.app.workspace.domain import Package as WPackage
from sat.app.workspace.domain import Project as WProject
from sat.app.workspace.domain import SourceFile as WSourcefile
import itertools


class Project(WProject):
    def __init__(self, abs_path, rel_path, name, packages):
        WProject.__init__(self, abs_path, rel_path, name, packages)
        child_changes = [p.changes for p in packages]
        self.changes = list(itertools.chain.from_iterable(child_changes))
        self.lines_added = sum([change.lines_added for change in self.changes])
        self.lines_removed = sum([change.lines_removed for change in self.changes])
        self.changes_total = self.lines_added + self.lines_removed
        self.num_contributer = len(set([c.committer for c in self.changes]))


class Package(WPackage):
    def __init__(self, abs_path, rel_path, name, sourcefiles):
        WPackage.__init__(self, abs_path, rel_path, name, sourcefiles)
        child_changes = [s.changes for s in sourcefiles]
        self.changes = list(itertools.chain.from_iterable(child_changes))
        self.lines_added = sum([change.lines_added for change in self.changes])
        self.lines_removed = sum([change.lines_removed for change in self.changes])
        self.changes_total = self.lines_added + self.lines_removed
        self.num_contributer = len(set([c.committer for c in self.changes]))


class SourceFile(WSourcefile):
    def __init__(self, abs_path, rel_path, name, changes, ast=None):
        WSourcefile.__init__(self, abs_path, rel_path, name, ast)
        self.changes = changes
        self.lines_added = sum([change.lines_added for change in self.changes])
        self.lines_removed = sum([change.lines_removed for change in self.changes])
        self.changes_total = self.lines_added + self.lines_removed
        self.num_contributer = len(set([c.committer for c in self.changes]))
        self.num_fixes = len([change for change in self.changes if change.is_fix])


class Change:
    def __init__(
        self, path, lines_added, lines_removed, committer, date, day_of_week, is_fix
    ):
        self.path = path
        self.lines_added = int(lines_added)
        self.lines_removed = int(lines_removed)
        self.changes_total = self.lines_added + self.lines_removed
        self.committer = committer
        self.date = date
        self.day_of_week = day_of_week
        self.is_fix = is_fix
