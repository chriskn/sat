
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging


class Analyser(ABC):
    
    @staticmethod
    @abstractmethod
    def name(Analysis):
        pass

    @property
    def _logger(self):
        return logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_data(self, workingDir, ignoredPathSegments):
        pass

    @abstractmethod
    def analyse(self, ignoredPathSegments):
        pass

    @abstractmethod
    def write_results(self, outputFolder):
        pass
