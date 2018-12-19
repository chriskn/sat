#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import subprocess
from domain import Change

_logger = logging.getLogger("Changerepo")
_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")
_changes_by_dir = dict()

def get_file_changes(workingdir, since):
    existing_changes =  _changes_by_dir.get(workingdir)
    if existing_changes:
        return existing_changes
    changes = []
    command = 'git log --numstat --oneline --shortstat --after="' + \
        since+'" -- ' + workingdir
    result = _run_git_command(command, workingdir)
    lines = result.splitlines()
    for line in lines:
        decoded = line.decode('utf-8')
        if _LINES_CHANGED_PATTERN.match(decoded):
            split = decoded.split("\t")
            changes.append(
                Change(int(split[0]), int(split[1]), split[2]))
    _changes_by_dir[workingdir] = changes
    return changes


def _run_git_command(command, workingdir):
    _logger.info("Running git command: %s", command)
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, cwd=workingdir, shell=True)
    except OSError as ose:
        _logger.warn("Error while executing git command: "+str(ose))
        return ""
    except subprocess.CalledProcessError as pe:
        _logger.warn("Error while executing git command: "+pe.output)
        return ""
    return result.stdout
