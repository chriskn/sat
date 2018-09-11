#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re
from project.project import Project
from project.project import Package
from project.project import SourceFile
import xml.etree.ElementTree
import javalang
from javalang.tree import Import
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration


class ProjectParser:    
    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignoredPathSegments = ignoredPathSegments

    def parseProjects(self):
        projetcPaths = self._scanForProjects()
        projects = [self._parseProject(projectPath) for projectPath in projetcPaths]
        return projects

    def _scanForProjects(self):
        projects = []
        for dirpath, dirNames, files in os.walk(self.directory):
            ignored = any(ignoredSegment in dirpath for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                for file in files:
                    if file == ".classpath": 
                        projects.append(dirpath)
        return projects

    def _parseProject(self, projectPath):
        classpathFilePath = os.path.join(projectPath,".classpath")
        relativeSourceFolders = self._parseClasspath(classpathFilePath)
        sourceFolders = [os.path.join(projectPath, s) for s in relativeSourceFolders]
        javaSourcePackages = self._parseJavaSourcePackages(sourceFolders)
        project = Project(os.path.basename(projectPath), projectPath, javaSourcePackages)
        return project

    def _parseJavaSourcePackages(self, sourceFolders):
        sourcePackages = []
        for sourceFolder in sourceFolders:
            for dirPath, dirName, files in os.walk(sourceFolder):
                javaFileNames = [file for file in files if file.endswith(".java")]
                if javaFileNames: 
                    packageName = os.path.normpath(dirPath.replace(sourceFolder,""))
                    packageName = ".".join(packageName.strip(os.sep).split(os.sep))
                    sourceFiles = []
                    for javaFile in javaFileNames:
                        sourceFile = self._parseJavaSourceFile(os.path.join(dirPath,javaFile))
                        if sourceFile:
                            sourceFiles.append(sourceFile)
                        
                    newPackage = Package(packageName, dirPath, sourceFiles)
                    sourcePackages.append(newPackage)
        #for sP in sourcePackages:
         #   for sF in sP.sourceFiles:
          #      sourceFiles = self._parseJavaSourceFile(os.path.join(sP.location,sF))
           #     sP.sourceFiles = sourceFiles
        return sourcePackages

    def _parseJavaSourceFile(self,file):
        fileContent = None
        try: 
            with open(file,'r', encoding='utf-8') as f:
                fileContent = f.read()
        except FileNotFoundError:
             print("Could not find file %s" %file)
             return
        ast = javalang.parse.parse(fileContent)
        packageImports = set()
        for imp in ast.imports:
            if imp.wildcard:
                packageImports.add(imp.path)
            else:
                package = re.split(r'\.[A-Z]',imp.path, maxsplit=1)[0]
                packageImports.add(package)
        concreteClasses = [type.name for type in ast.types if isinstance(type, ClassDeclaration) and 'abstract' not in type.modifiers]
        abstractClasses = [type.name for type in ast.types if isinstance(type, ClassDeclaration) and 'abstract' in type.modifiers]
        interfaces = [type.name for type in ast.types if isinstance(type, InterfaceDeclaration)]
        filename, extension = os.path.splitext(os.path.basename(file))
        nonEmptyLines = [line for line in fileContent.splitlines() if line.strip()]
        loc = len(nonEmptyLines)
        return SourceFile(filename, extension[1:], packageImports, loc, concreteClasses, abstractClasses, interfaces)

    def _parseClasspath(self, classpathFilePath):
        sourceFolders = []
        root = xml.etree.ElementTree.parse(classpathFilePath).getroot()
        for classpath in root.findall('classpathentry'):
            if classpath.get('kind') == "src":
                sourceFolders.append(classpath.get('path'))
        return sourceFolders
        '''
        content = None 
        with open(classpathFilePath,'r') as f:
            content = f.read()
        lines = content.splitlines()
        for line in lines:
            stripped = line.strip(" ").strip("\t")
            if "classpathentry" in stripped and 'kind="src"' in stripped:
                print(stripped)
                stripped."*[@id='{0}']//"
        '''

