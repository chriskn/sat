#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sat.changes.changeparser as parser

_CHANGES_BY_DIR = dict()


def changes(workingdir, since):
    existing_changes = _CHANGES_BY_DIR.get(workingdir)
    if existing_changes:
        return existing_changes
    changes_for_dir = parser.parse_changes(workingdir, since)
    _CHANGES_BY_DIR[workingdir] = changes_for_dir
    return changes_for_dir
