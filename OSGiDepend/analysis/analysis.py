#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging

class Analysis(ABC):

    @property
    def logger(self):
        return logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def loadData(self, workingDir, ignoredPathSegments):
        pass   

    @abstractmethod
    def analyse(self, ignoredPathSegments):
        pass 

    @abstractmethod
    def writeResults(self, outputFolder):
        pass    

    @abstractmethod
    def getName(self):
        pass    
    
    @abstractmethod
    def getDescription(self):
        pass 