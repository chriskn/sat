#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Change():

    def __init__(self, path, lines_added, lines_removed):
        self.path = path
        self.lines_added = int(lines_added)
        self.lines_removed = int(lines_removed)
        self.total_lines = self.lines_added+self.lines_removed
