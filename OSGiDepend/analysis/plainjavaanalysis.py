#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
from project.projectgraph import ProjectGraph 
from package.packagegraph import PackageGraph 
from analysis.analysis import Analysis
import numpy as np
import pandas as pd
import os
import plot

class PlainJavaAnalyser(Analysis):

    _LIST_SEPARATOR = ", " 

    def getName(self):
        return "javaDeps"
    
    def getDescription(self):
        return "Analysis plain java dependiencies for projects and packages (based on classpath files)"

    def loadData(self, workingDir, ignoredPathSegments):
        self.logger.info("Loading project data...") 
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parseProjects()
        self._projects = projects
        self._packages = []
        for p in self._projects:
            self._packages.extend(p.sourcePackages)

    def analyse(self, ignoredPathSegments): 
        self.logger.info("Creating project coupling graph")
        self._projectGraph = ProjectGraph(self._projects)
        self.logger.info("Analysing project cycles")
        self._projectCycles = self._projectGraph.getCycles()
        self._projectGraph.markCycles(self._projectCycles)
        self._cycleProjectGraph =  self._projectGraph.getCycleGraph(self._projectCycles)
        self.logger.info("Creating project coupling map")
        self._projectCouplingMap = self._createProjectCouplingDataFrame(self._projects)
        
        self.logger.info("Creating package coupling graph")
        self._packageGraph = PackageGraph(self._packages)
        self.logger.info("Analysing package cycles")
        self._packageCycles = self._packageGraph.getCycles()
        self._packageGraph.markCycles(self._packageCycles)
        self._cyclePackageGraph =  self._packageGraph.getCycleGraph(self._packageCycles)   
        self.logger.info("Creating package coupling map")
        self._packageCouplingMap = self._createPackageCouplingDataFrame(self._packages)
        
        self.logger.info("Analysed %d projects" %len(self._projects)) 
        self.logger.info("Analysed %d packages" %len(self._packages)) 

    def writeResults(self, outputDir):
        self.logger.info("Writing project analysis results")
        plot.plotHeatmap(self._projectCouplingMap, "Project Coupling", outputDir, "project_coupling_heatmap.pdf")
        self._writeGraphToGraphMl(os.path.join(outputDir,"project_dependencies.graphml"), self._projectGraph)
        self._writeGraphToGraphMl(os.path.join(outputDir,"cyclic_project_dependencies.graphml"), self._cycleProjectGraph)
        self._writeCyclesToTxt(os.path.join(outputDir,"project_cycles.txt"), self._projectCycles)

        self.logger.info("Writing package analysis results")
        plot.plotHeatmap(self._packageCouplingMap, "Package Coupling", outputDir, "package_coupling_heatmap.pdf")
        self._writeGraphToGraphMl(os.path.join(outputDir,"package_dependencies.graphml"), self._packageGraph)
        self._writeGraphToGraphMl(os.path.join(outputDir,"cyclic_package_dependencies.graphml"), self._cyclePackageGraph)
        self._writeCyclesToTxt(os.path.join(outputDir,"package_cycles.txt"), self._packageCycles)


    def _createProjectCouplingDataFrame(self, projects):
        pNames = []
        data = []
        for project in reversed(projects):
            pImports = project.getImports()
            pNames.append(project.name)
            projData = []
            for oProject in projects:
                projDeps = 0
                for oPackage in oProject.sourcePackages:
                    occurences = pImports.count(oPackage.name)
                    projDeps += occurences
                projData.append(projDeps)    
            data.append(projData)
        return pd.DataFrame(data=data, index=pNames, columns=list(reversed(pNames)))

    def _writeGraphToGraphMl(self, path, graph):
        with open(path, 'w') as outputFile:
            outputFile.write(graph.serialize())

    def _writeCyclesToTxt(self, path, cycles):
        with open(path, 'w') as outputFile:
            for cycle in cycles: 
                cycleList = self._LIST_SEPARATOR.join(sorted(cycle))
                outputFile.write(cycleList+"\n")

    def _createPackageCouplingDataFrame(self, packages):
        names = [p.name for p in packages]
        data = []
        for package in reversed(packages):
            data.append([package.getImports().count(pName) for pName in names])
        return pd.DataFrame(data=data, index=list(reversed(names)), columns=names)