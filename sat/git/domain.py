#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Change():

    def __init__(self, lines_added, lines_removed, filepath):
        self.lines_added = lines_added
        self.lines_removed = lines_removed
        self.filepath = filepath
