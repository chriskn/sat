#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xmltree


def parse_classpath(classpath_file_path):
    sourcefolders = []
    root = xmltree.parse(classpath_file_path).getroot()
    for classpath in root.findall("classpathentry"):
        if classpath.get("kind") == "src":
            sourcefolders.append(classpath.get("path"))
    return sourcefolders
