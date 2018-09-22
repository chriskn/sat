#!/usr/bin/env python
# -*- coding: utf-8 -*-

from domain import SourceFile
from javalang.tree import Import
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration
from javalang.parser import JavaSyntaxError
import javalang, os, re, logging


classNamePattern = re.compile(r'.*\.[A-Z].*')
logger = logging.getLogger(__name__)

def parseJavaSourceFile(file):
        fileContent = None
        try: 
            with open(file,'r', encoding='utf-8') as f: fileContent = f.read()
            ast = javalang.parse.parse(fileContent)
        except FileNotFoundError as error:
            logger.warn(str(error))
            return
        except JavaSyntaxError:
            logger.warn("Could not parse java file %s" % file)
            return
        packageImports = set()
        for imp in ast.imports:
            if classNamePattern.match(imp.path):
                package = re.split(r'\.[A-Z]',imp.path, maxsplit=1)[0]
                packageImports.add(package)
            else:
                packageImports.add(imp.path)
        concreteClasses = [type.name for type in ast.types if isinstance(type, ClassDeclaration) and 'abstract' not in type.modifiers]
        abstractClasses = [type.name for type in ast.types if isinstance(type, ClassDeclaration) and 'abstract' in type.modifiers]
        interfaces = [type.name for type in ast.types if isinstance(type, InterfaceDeclaration)]
        filename, extension = os.path.splitext(os.path.basename(file))
        nonEmptyLines = [line for line in fileContent.splitlines() if line.strip()]
        loc = len(nonEmptyLines)
        return SourceFile(filename, extension[1:], packageImports, loc, concreteClasses, abstractClasses, interfaces)