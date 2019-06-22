# -*- coding: utf-8 -*-
import re
import logging
import subprocess
import os
from sat.changes.domain import Change

_LOGGER = logging.getLogger("ChangeRepo")
_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")


def parse_changes(workingdir, since):
    changes_for_dir = []
    command = (
        'git log --numstat --oneline --shortstat --after="'
        + since
        + '" -- '
        + workingdir
    )
    result = _run_git_command(command, workingdir)
    lines = result.splitlines()
    for line in lines:
        decoded = line.decode("utf-8")
        if _LINES_CHANGED_PATTERN.match(decoded):
            change = _parse_change(decoded)
            changes_for_dir.append(change)
    return changes_for_dir


def _parse_change(decoded):
    split = decoded.split("\t")
    path = os.path.normpath(split[2])
    lines_added = int(split[0])
    lines_removed = int(split[1])
    return Change(path, lines_added, lines_removed)


def _run_git_command(command, workingdir):
    _LOGGER.info("Running git command: %s", command)
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, cwd=workingdir, shell=True
        )
        return result.stdout
    except OSError as ose:
        _LOGGER.warning("OS Error while executing git command: %s", str(ose))
    except subprocess.CalledProcessError as process_error:
        _LOGGER.warning(
            "Process Error while executing git command. Return Code %s",
            str(process_error.returncode),
        )
    return ""
