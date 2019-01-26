#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import subprocess
import os
from changes.domain import Change

_logger = logging.getLogger("ChangeRepo")
_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")
_changes_by_dir = dict()


def changes(workingdir, since):
    existing_changes = _changes_by_dir.get(workingdir)
    if existing_changes:
        return existing_changes
    changes = _parse_changes(workingdir, since)
    _changes_by_dir[workingdir] = changes
    return changes


def _parse_changes(workingdir, since):
    changes = []
    command = 'git log --numstat --oneline --shortstat --after="' + \
        since + '" -- ' + workingdir
    result = _run_git_command(command, workingdir)
    lines = result.splitlines()
    for line in lines:
        decoded = line.decode('utf-8')
        if _LINES_CHANGED_PATTERN.match(decoded):
            split = decoded.split("\t")
            path = os.path.normpath(split[2])
            lines_added = int(split[0])
            lines_removed = int(split[1])
            changes.append(
                Change(path, lines_added, lines_removed)
            )
    return changes


def _run_git_command(command, workingdir):
    _logger.info("Running git command: %s", command)
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, cwd=workingdir, shell=True)
        return result.stdout
    except OSError as ose:
        _logger.warning("OS Error while executing git command: " + str(ose))
    except subprocess.CalledProcessError as pe:
        _logger.warning(
            "Process Error while executing git command. Return Code " + str(pe.returncode))
    return ""
