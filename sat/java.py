#!/usr/bin/env python
# -*- coding: utf-8 -*-

import javalang
from javalang.parser import JavaSyntaxError
import logging

logger = logging.getLogger(__name__)


def parse(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
            return javalang.parse.parse(file_content)
    except FileNotFoundError as error:
        logger.warn(str(error))
        return
    except JavaSyntaxError:
        logger.warn("Could not parse java file %s. Invalid syntax" % file)
        return
