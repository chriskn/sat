#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import subprocess
import os
from changes.domain import Change

_LOGGER = logging.getLogger("ChangeRepo")
_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")
_CHANGES_BY_DIR = dict()


def changes(workingdir, since):
    existing_changes = _CHANGES_BY_DIR.get(workingdir)
    if existing_changes:
        return existing_changes
    num_changes = _parse_changes(workingdir, since)
    _CHANGES_BY_DIR[workingdir] = num_changes
    return num_changes


def _parse_changes(workingdir, since):
    changes_for_dir = []
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
            changes_for_dir.append(
                Change(path, lines_added, lines_removed)
            )
    return changes_for_dir


def _run_git_command(command, workingdir):
    _LOGGER.info("Running git command: %s", command)
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, cwd=workingdir, shell=True)
        return result.stdout
    except OSError as ose:
        _LOGGER.warning("OS Error while executing git command: %s", str(ose))
    except subprocess.CalledProcessError as process_error:
        _LOGGER.warning(
            "Process Error while executing git command. Return Code %s", str(process_error.returncode))
    return ""
