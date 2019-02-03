#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import javalang
from javalang.parser import JavaSyntaxError

_LOGGER = logging.getLogger(__name__)


def parse(file_):
    try:
        with open(file_, 'r', encoding='utf-8') as open_file:
            file_content = open_file.read()
            return javalang.parse.parse(file_content)
    except FileNotFoundError as error:
        _LOGGER.warnng(str(error))
        return None
    except JavaSyntaxError:
        _LOGGER.warning("Could not parse java file %s. Invalid syntax", file_)
        return None
