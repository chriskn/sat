#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
from project.projectgraph import ProjectGraph 
import numpy as np
import pandas as pd
import os
import plot

class ProjectAnalyser:

    _projects = None
    _projectGraph = None 
    _cycleProjectGraph = None 
    _projectCouplingMap = None

    def analyse(self, workingDir, ignoredPathSegments): 
        print("Analysing projects...") 
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parseProjects()
        self._projects = projects
        print("Creating project coupling graph")
        projectGraph = ProjectGraph(projects)
        print("Analysing project cycles")
        cycles = projectGraph.getCycles()
        projectGraph.markCycles(cycles)
        self._projectGraph = projectGraph
        self._cycleProjectGraph =  projectGraph.getCycleGraph(cycles)
        '''
        packages = []
        for p in self._projects:
            packages.extend(p.sourcePackages)
        packageGraph = PackageGraph(packages)
        cycles = packageGraph.getCycles()
        packageGraph.markCycles(cycles)
        self._packageGraph = packageGraph
        self._cyclePackageGraph =  packageGraph.getCycleGraph(cycles)   
        '''
        print("Creating project coupling map")
        self._projectCouplingMap = self._createProjectCouplingDataFrame(projects)
        print("Analysed %d projects" %len(projects)) 

    def writeResults(self, outputDir):
        print("Writing project analysis results")
        plot.plotHeatmap(self._projectCouplingMap, "Project Coupling", outputDir, "project_coupling_heatmap.pdf")
        self._writeGraphToGraphMl(os.path.join(outputDir,"project_dependencies.graphml"), self._projectGraph)
        self._writeGraphToGraphMl(os.path.join(outputDir,"cyclic_project_dependencies.graphml"), self._cycleProjectGraph)

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
'''
    def _createPackageCouplingHeatmap(self,outputFolder):
        print("Creating package coupling heatmap...")
        packages = []
        for p in self._projects:
            packages.extend(p.sourcePackages)
        heatmapFig = self._buildCouplingHeatmap(packages, "Package Coupling")
        heatmapPath = os.path.join(outputFolder,"package_coupling_heatmap.pdf")
        print("Writing coupling heatmap...")
        heatmapFig.savefig(heatmapPath, bbox_inches = 'tight')
        plt.close(heatmapFig)
        print("Wrote coupling heatmap to %s" %heatmapPath)

    def _writeProjectCouplingHeatmap(self, outputFolder):
        heatmapFig = self._buildPCouplingHeatmap(self._projects, "Project Coupling")
        heatmapPath = os.path.join(outputFolder,"project_coupling_heatmap.pdf")
        print("Writing coupling heatmap...")
        heatmapFig.savefig(heatmapPath, bbox_inches = 'tight')
        plt.close(heatmapFig)
        print("Wrote coupling heatmap to %s" %heatmapPath)
 
    def _buildCouplingHeatmap(self, packages, title):
        names = [p.name for p in packages]
        data = []
        for package in reversed(packages):
            data.append([package.getImports().count(pName) for pName in names])
        df = pd.DataFrame(data=data, index=list(reversed(names)), columns=names)
        return self._buildHeatMap(df, title)
'''