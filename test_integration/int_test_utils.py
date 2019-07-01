#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sat.__main__ as main

_ROOT_LOCATION = os.path.dirname(os.path.dirname(os.path.abspath(main.__file__)))
EXAMPLE_PROJECTS_LOCATION = os.path.join(_ROOT_LOCATION, "sample")
