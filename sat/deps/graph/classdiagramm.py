#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sat.deps.domain import Class, Enum, Interface
from sat.deps.graph.graph import Graph
import sat.deps.graph.cyclegraph as cyclegraph


_BUILD_IN_TYPES = ["int", "boolean", "String", "double", "float", "byte"]
_LOGGER = logging.getLogger(__name__)


class ClassDiagramm(Graph):
    def __init__(self, packages):
        Graph.__init__(self)
        (top_level_elements, self._imports_for_fqn) = _collect_top_level_elements(
            packages
        )
        self._elements_by_fqn = {tle.fqn: tle for tle in top_level_elements}
        for package in packages:
            self._add_package(package)
        for tle in top_level_elements:
            external_deps = set(_filter_external_types(tle))
            # if type_ in simple_names
            for type_ in external_deps:
                self._add_dependency(tle, type_)
            if isinstance(tle, Class):
                if tle.extends:
                    self._add_dependency(tle, tle.extends, arrowhead="white_delta")
                for interface in tle.implements:
                    self._add_dependency(
                        tle, interface, line_type="dotted", arrowhead="white_delta"
                    )
            if isinstance(tle, Interface):
                if tle.extends:
                    self._add_dependency(tle, tle.extends, arrowhead="white_delta")

    def _add_dependency(self, tle, dependency, line_type="line", arrowhead="standard"):
        possible_fqns_for_dependency = [
            key for key, val in self._elements_by_fqn.items() if val.name == dependency
        ]
        if len(possible_fqns_for_dependency) == 1:
            self.add_edge(
                tle.fqn,
                possible_fqns_for_dependency[0],
                line_type=line_type,
                arrowhead=arrowhead,
            )
        elif len(possible_fqns_for_dependency) > 1:
            imports_for_node = self._imports_for_fqn[tle.fqn]
            fqn_deps = imports_for_node.intersection(possible_fqns_for_dependency)
            if len(fqn_deps) == 1:
                self.add_edge(
                    tle.fqn, list(fqn_deps)[0], line_type=line_type, arrowhead=arrowhead
                )
            elif fqn_deps:
                _LOGGER.warning(
                    "Multiple alternative dependencies from node %s to possible alternatives: %s",
                    tle.fqn,
                    ",".join(fqn_deps),
                )
        # else:
        # logger.warn("Can't find dependency from node %s to possible alternatives: %s" % (tle.fqn, dependency))

    def _add_package(self, package):
        package_group = self.add_group(package.name, shape="rectangle", fill="#ffd35b")
        for sourcefile in package.sourcefiles:
            for con_class in sourcefile.concrete_classes:
                self._add_class(con_class, package_group)
            for abstr_class in sourcefile.abstract_classes:
                self._add_abstract_class(abstr_class, package_group)
            for interface in sourcefile.interfaces:
                self._add_interface(interface, package_group)
            for enum in sourcefile.enums:
                self._add_enum(enum, package_group)

    def _add_interface(self, interface, package_group):
        uml = _uml(interface)
        self.add_node(
            interface.name,
            package_group,
            node_type="UMLClassNode",
            shape_fill="#FFFFFF",
            uml=uml,
        )

    def _add_enum(self, enum, package_group):
        uml = {
            "attributes": "\n".join(enum.constants),
            "methods": "",
            "stereotype": "enum",
        }
        self.add_node(
            enum.name,
            package_group,
            node_type="UMLClassNode",
            shape_fill="#FFFFFF",
            uml=uml,
        )

    def _add_abstract_class(self, clazz, package_group):
        uml = _uml(clazz)
        self.add_node(
            clazz.name,
            package_group,
            node_type="UMLClassNode",
            shape_fill="#FFFFFF",
            uml=uml,
        )

    def _add_class(self, clazz, package_group):
        uml = _uml(clazz)
        self.add_node(
            clazz.name,
            package_group,
            node_type="UMLClassNode",
            shape_fill="#FFFFFF",
            uml=uml,
        )

    def cycle_graph(self, cycles):
        graph = ClassDiagramm([])
        cyclegraph.create(graph, self, cycles, grouped=True)
        return graph


def _uml(type_):
    attributes = [_declaration_to_string(attribute) for attribute in type_.attributes]
    methods = [_method_to_string(method) for method in type_.methods]
    return {
        "attributes": "\n".join(attributes),
        "methods": "\n".join(methods),
        "stereotype": type_.stereotype,
    }


def _method_to_string(method):
    params = [_declaration_to_string(param).strip(" ") for param in method.parameters]
    modifiers = [_visibility(modifier) for modifier in method.modifiers]
    static = _static_prefix(method.modifiers)
    abstract = _abstract_prefix(method.modifiers)
    method_str = "{0}{1} {2}{3}({4}): {5}".format(
        abstract,
        static,
        "".join(modifiers),
        method.name,
        ", ".join(params),
        method.return_type_name,
    )
    return method_str


def _declaration_to_string(attribute):
    modifiers = "".join([_visibility(modifier) for modifier in attribute.modifiers])
    static = _static_prefix(attribute.modifiers)
    abstract = _abstract_prefix(attribute.modifiers)
    return "{0}{1} {2}{3}: {4}".format(
        abstract, static, modifiers, attribute.name, attribute.typename
    )


def _collect_top_level_elements(packages):
    imports_for_fqn = dict()
    top_level_elements = []
    for package in packages:
        for sourcefile in package.sourcefiles:
            tles_for_file = sourcefile.tles
            imports_for_fqn.update(
                {tle.fqn: sourcefile.imports for tle in tles_for_file}
            )
            top_level_elements.extend(tles_for_file)
    return (top_level_elements, imports_for_fqn)


def _filter_external_types(class_):
    if not isinstance(class_, Enum):
        types_for_attributes = list(
            filter(lambda attr: attr.typename not in _BUILD_IN_TYPES, class_.attributes)
        )
        types_for_attributes[:] = [
            type.typename for type in types_for_attributes if type.typename != "enum"
        ]
        types_for_params = []
        for method in class_.methods:
            types_for_params.extend(
                list(
                    filter(
                        lambda param: param.typename not in _BUILD_IN_TYPES,
                        method.parameters,
                    )
                )
            )
        types_for_params[:] = [type.typename for type in types_for_params]
        return types_for_attributes + types_for_params
    return []


def _filter_parents(class_):
    parents = [class_.extends.name] if class_.extends else []
    if not isinstance(class_, Interface) and class_.implements:
        parents.extend([interface.name for interface in class_.implements])
    return parents


def _visibility(modifier):
    visibility_switch = {"public": "+", "private": "-", "protected": "~"}
    return visibility_switch.get(modifier, "")


def _static_prefix(modifiers):
    return "s" if "static" in modifiers else " "


def _abstract_prefix(modifiers):
    return "a" if "abstract" in modifiers else " "
