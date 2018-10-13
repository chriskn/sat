#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyyed
from domain import Interface
from domain import Enum
from graph import Graph
import textwrap

BUILD_IN_TYPES = ["int", "boolean", "String", "double", "float"]


class ClassDiagramm(Graph):

    _INTERFACE_STEREOTYPE = "interface"

    def __init__(self, packages):
        Graph.__init__(self)
        toplevel_elements = self._collect_top_level_elements(packages)
        self._elements_by_fqn = dict()
        for tle in toplevel_elements:
            self._elements_by_fqn[tle.fqn] = tle
        for package in packages:
            self._add_package(package)
        toplevel_element_names = [tle.name for tle in toplevel_elements]
        for tle in toplevel_elements:
            external_deps = set(self._filter_external_types(tle))
            external_deps_in_graph = [
                external_dep for external_dep in external_deps if external_dep in toplevel_element_names]
            for external_dep in external_deps_in_graph:
                fqns = [key for key,val in self._elements_by_fqn.items() if val.name == external_dep]
                if len(fqns) == 1:
                    self.add_edge(tle.fqn, fqns[0])
                elif len(fqns) > 1:
                    print(fqns)

                    


    def _collect_top_level_elements(self, packages):
        elements = []
        for package in packages:
            for sourcefile in package.sourcefiles:
                elements.extend(sourcefile.concrete_classes)
                elements.extend(sourcefile.abstract_classes)
                elements.extend(sourcefile.interfaces)
                elements.extend(sourcefile.enums)
        return elements

    def _filter_external_types(self, class_):
        if not type(class_) is Enum:
            types_for_attributes = list(
                filter(lambda attr: attr.typename not in BUILD_IN_TYPES, class_.attributes))
            types_for_attributes[:] = [
                type.typename for type in types_for_attributes if type.typename != "enum"]
            types_for_params = []
            for method in class_.methods:
                types_for_params.extend(list(
                    filter(lambda param: param.typename not in BUILD_IN_TYPES, method.parameters)))
            types_for_params[:] = [type.typename for type in types_for_params]
            return types_for_attributes+types_for_params
        return []

    def _filter_parents(self, class_):
        parents = [class_.extends.name] if class_.extends else []
        if not isinstance(class_, Interface) and class_.implements:
            parents.extend([interface.name for interface in class_.implements])
        return parents

    def _add_package(self, package):
        package_group = self.add_group(
            package.name, shape="rectangle", fill="#ffd35b")
        for sourcefile in package.sourcefiles:
            for con_class in sourcefile.concrete_classes:
                self._add_class(con_class, package_group)
            for abstr_class in sourcefile.abstract_classes:
                self.add_abstract_class(abstr_class, package_group)
            for interface in sourcefile.interfaces:
                self._add_interface(interface, package_group)
            for enum in sourcefile.enums:
                self._add_enum(enum, package_group)

    def _add_interface(self, interface, packageGroup):
        uml = self._UML(interface)
        self.add_node(interface.name, packageGroup, node_type="UMLClassNode",
                      shape_fill="#FFFFFF", UML=uml)

    def _add_enum(self, enum, package_group):
        uml = {"attributes": "\n".join(
            enum.constants), "methods": "", "stereotype": "enum"}
        self.add_node(enum.name, package_group, node_type="UMLClassNode",
                      shape_fill="#FFFFFF", UML=uml)

    def add_abstract_class(self, clazz, package_group):
        uml = self._UML(clazz)
        self.add_node(clazz.name, package_group, node_type="UMLClassNode",
                      shape_fill="#FFFFFF", UML=uml)

    def _add_class(self, clazz, package_group):
        uml = self._UML(clazz)
        self.add_node(
            clazz.name, package_group, node_type="UMLClassNode", shape_fill="#FFFFFF", UML=uml)

    def _UML(self, type):
        attributes = [self._declaration_to_string(
            attribute) for attribute in type.attributes]
        methods = [self._method_to_String(method) for method in type.methods]
        return {"attributes": "\n".join(attributes),
                "methods": "\n".join(methods),
                "stereotype": type.stereotype}

    def _method_to_String(self, method):
        params = [self._declaration_to_string(param).strip(
            " ") for param in method.parameters]
        modifiers = [self._visibility(modifier)
                     for modifier in method.modifiers]
        static = self.getStaticPrefix(method.modifiers)
        abstract = self.getAbstractPrefix(method.modifiers)
        method_str = "{0}{1} {2}{3}({4}): {5}".format(abstract, static, "".join(
            modifiers), method.name, ", ".join(params), method.return_type_name)
        return method_str

    def _declaration_to_string(self, attribute):
        modifiers = "".join([self._visibility(modifier)
                             for modifier in attribute.modifiers])
        static = self.getStaticPrefix(attribute.modifiers)
        abstract = self.getAbstractPrefix(attribute.modifiers)
        return "{0}{1} {2}{3}: {4}".format(abstract, static, modifiers, attribute.name, attribute.typename)

    def _visibility(self, modifier):
        visibilitySwitch = {
            "public": "+",
            "private": "-",
            "protected": "~"
        }
        return visibilitySwitch.get(modifier, "")

    def getStaticPrefix(self, modifiers):
        return "s" if "static" in modifiers else " "

    def getAbstractPrefix(self, modifiers):
        return "a" if "abstract" in modifiers else " "
