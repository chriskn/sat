# -*- coding: utf-8 -*-
import re
import logging
import subprocess
import os
from sat.changes.domain import Change

_LOGGER = logging.getLogger("ChangeParser")
_BLANK_LINE_REGEX = re.compile(r"(?:\r?\n){2,}")
_FIX_INDACTORS = ["fix", "fixes", "bugfix", "bug-fix"]


def parse_changes(workingdir, since):
    git_changes_str = _execute_git_log(workingdir, since).decode("utf-8")
    git_changes = re.split(_BLANK_LINE_REGEX, git_changes_str.strip())
    changes_for_file = dict()
    for git_change in git_changes:
        committer = ""
        date = ""
        day_of_week = ""
        for index, line in enumerate(git_change.splitlines()):
            if index == 0:
                committer, date, day_of_week, is_fix = _parse_summary(line)
            else:
                path, lines_added, lines_removed = _parse_change(line, workingdir)
                if lines_added + lines_removed > 0:
                    if path in changes_for_file:
                        changes_for_file[path].append(
                            Change(
                                path,
                                lines_added,
                                lines_removed,
                                committer,
                                date,
                                day_of_week,
                                is_fix,
                            )
                        )
                    else:
                        changes_for_file[path] = [
                            Change(
                                path,
                                lines_added,
                                lines_removed,
                                committer,
                                date,
                                day_of_week,
                                is_fix,
                            )
                        ]

    return changes_for_file


def _parse_change(line, workingdir):
    split = line.split("\t")
    return (
        os.path.normpath(os.path.join(workingdir, split[2])),
        int(split[0]) if split[0].isdigit() else 0,
        int(split[1]) if split[1].isdigit() else 0,
    )


def _parse_summary(line):
    split = line.split(" ")
    message = " ".join(split[4 : len(split)]).lower()
    return (
        split[0],
        split[1],
        split[2],
        any([fix_indicator in message for fix_indicator in _FIX_INDACTORS]),
    )


def _execute_git_log(workingdir, since):
    command_str = """git log 
    --pretty=format:"%%ce %%cd %%s"
    --date=format:"%%Y-%%m-%%d %%a" 
    --numstat  
    --after=%s 
    --no-merges
    -- %s
    """ % (
        since,
        workingdir,
    )
    command = " ".join([line.strip() for line in command_str.splitlines()])
    return _execute_command(command, workingdir)


def _execute_command(command, workingdir):
    _LOGGER.info("Running command: %s", command)
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
