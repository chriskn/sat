#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913

from abc import ABC, abstractmethod


class Executer(ABC):
    def __init__(self, analysers, workspace, output_dir):
        self._workspace = workspace
        self._output_dir = output_dir
        self._analyser_cls_by_name = {
            analyser.name(): analyser for analyser in analysers
        }

    def execute(self, analysers_to_execute):
        for analyser_name in analysers_to_execute:
            analyser = self._init_analysers(analyser_name)
            analyser.load_data()
            analyser.analyse()
            analyser.write_results(self._output_dir)

    def _init_analysers(self, analyser_name):
        analysercls = self._analyser_cls_by_name[analyser_name]
        return analysercls(self._workspace)

    @staticmethod
    @abstractmethod
    def args():
        pass


class ExecuterArgs:
    def __init__(self, name, analyser_names, description, options=None):
        self.name = name
        self.analyser_names = analyser_names
        self.description = description
        self.options = options if options else []


class Option:
    def __init__(self, argument, destination, description, default=None, required=True):
        self.argument = argument
        self.dest = destination
        self.metavar = destination
        self.default = default
        self.required = required
        self.help = description
