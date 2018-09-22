#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import lang.java as javaParser
from domain import Package

class PackageParser: 

    def parsePackages(self, sourceFolders):
        sourcePackages = []
        for sourceFolder in sourceFolders:
            sourcePackages.extend(self.parsePackage(sourceFolder))
        return sourcePackages

    def parsePackage(self, sourceFolder):
        sourcePackages = []
        for dirPath, dirName, files in os.walk(sourceFolder):
            javaFileNames = [file for file in files if file.endswith(".java")]
            if javaFileNames:
                packageName = os.path.normpath(dirPath.replace(sourceFolder,""))
                packageName = ".".join(packageName.strip(os.sep).split(os.sep))
                sourceFiles = []
                for javaFile in javaFileNames:
                    sourceFile = javaParser.parseJavaSourceFile(os.path.join(dirPath,javaFile))
                    if sourceFile:
                        sourceFiles.append(sourceFile)
                newPackage = Package(packageName, dirPath, sourceFiles)
                sourcePackages.append(newPackage)
        return sourcePackages