#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from sat.deps.domain import Bundle


def parse(directory, ignored_path_segments):
    bundle_paths = _scan_for_bundles(directory, ignored_path_segments)
    bundles = sorted([_parse_bundle(bundlPath) for bundlPath in bundle_paths])
    return bundles


def _scan_for_bundles(directory, ignored_path_segments):
    bundels = set()
    for dirpath, _, files in os.walk(directory):
        ignored = any(
            ignored_segment in dirpath for ignored_segment in ignored_path_segments
        )
        if not ignored:
            for file in files:
                if file == "MANIFEST.MF":
                    bundels.add(os.path.dirname(dirpath))
    return bundels


def _parse_bundle(bundle_path):
    manifest_path = os.path.join(bundle_path, "META-INF", "MANIFEST.MF")
    symbolic_name, version, exported_packages, imported_packages, required_bundles = _parse_manifest(
        manifest_path
    )
    number_of_dependencies = len(required_bundles) + len(imported_packages)
    bundle = Bundle(
        bundle_path,
        symbolic_name,
        version,
        exported_packages,
        imported_packages,
        required_bundles,
        number_of_dependencies,
    )
    return bundle


def _parse_manifest(manifest_path):
    manifest_content = open(manifest_path, "rb").read().decode()
    entries = re.split(r"[\r\n]+(?!\s)", manifest_content)
    required_bundles = []
    imported_packages = []
    exported_packages = []
    version = ""
    symbolic_name = ""
    for entry in entries:
        if entry.startswith("Require-Bundle:"):
            required_bundles = [
                _trim(bundle) for bundle in _split_entries(entry, "Require-Bundle:")
            ]
        elif entry.startswith("Import-Package:"):
            imported_packages = [
                _trim(package) for package in _split_entries(entry, "Import-Package:")
            ]
        elif entry.startswith("Export-Package:"):
            # removes 'uses' declaration
            if ";" in entry:
                entry = entry[: entry.index(";")]
            exported_packages = [
                _trim(package) for package in _split_entries(entry, "Export-Package:")
            ]
        elif entry.startswith("Bundle-Version:"):
            version = _trim(entry.replace("Bundle-Version:", ""))
        elif entry.startswith("Bundle-SymbolicName:"):
            symbolic_name = _trim(entry.replace("Bundle-SymbolicName:", ""))
            if ";" in symbolic_name:
                symbolic_name = symbolic_name[: symbolic_name.index(";")]
    # remove additional information (ie. bundle-version)
    required_bundles[:] = [
        requiredBundle[: requiredBundle.index(";")]
        if ";" in requiredBundle
        else requiredBundle
        for requiredBundle in required_bundles
    ]
    return (
        symbolic_name,
        version,
        exported_packages,
        imported_packages,
        required_bundles,
    )


def _trim(str_):
    return str_.replace("\n", "").replace("\r", "").strip(" ")


def _split_entries(entry, entry_name):
    return re.split(r",(?!\d)", entry.replace(entry_name, ""))
