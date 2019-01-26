#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deps.domain import Bundle
import os
import re


class BundleParser:

    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignored_path_segments = ignoredPathSegments

    def parse(self):
        bundle_paths = self._scan_for_bundles()
        bundles = [self._parse_bundle(bundlPath) for bundlPath in bundle_paths]
        return bundles

    def _scan_for_bundles(self):
        bundels = set()
        for dirpath, dirnames, files in os.walk(self.directory):
            ignored = any(
                ignored_segment in dirpath for ignored_segment in self.ignored_path_segments)
            if not ignored:
                for file in files:
                    if file == "MANIFEST.MF":
                        bundels.add(os.path.dirname(dirpath))
        return bundels

    def _parse_bundle(self, bundle_path):
        manifest_path = bundle_path + "/META-INF/MANIFEST.MF"
        symbolic_name, version, exportedPackages, importedPackages, requiredBundles = self._parse_manifest(
            manifest_path)
        number_of_dependencies = len(requiredBundles) + len(importedPackages)
        bundle = Bundle(
            bundle_path,
            symbolic_name,
            version,
            exportedPackages,
            importedPackages,
            requiredBundles,
            number_of_dependencies)
        return bundle

    def _parse_manifest(self, manifest_path):
        manifest_content = open(manifest_path, 'rb').read().decode()
        entries = re.split(r'[\r\n]+(?!\s)', manifest_content)
        required_bundles = []
        imported_packages = []
        exported_packages = []
        version = ""
        symbolic_name = ""
        for entry in entries:
            if entry.startswith("Require-Bundle:"):
                required_bundles = [
                    self._trim(bundle) for bundle in self._splitEntries(
                        entry, "Require-Bundle:")]
            elif entry.startswith("Import-Package:"):
                imported_packages = [
                    self._trim(package) for package in self._splitEntries(
                        entry, "Import-Package:")]
            elif entry.startswith("Export-Package:"):
                # removes 'uses' declaration
                if ';' in entry:
                    entry = entry[:entry.index(';')]
                exported_packages = [
                    self._trim(package) for package in self._splitEntries(
                        entry, "Export-Package:")]
            elif entry.startswith("Bundle-Version:"):
                version = self._trim(entry.replace("Bundle-Version:", ""))
            elif entry.startswith("Bundle-SymbolicName:"):
                symbolic_name = self._trim(
                    entry.replace("Bundle-SymbolicName:", ""))
                if ";" in symbolic_name:
                    symbolic_name = symbolic_name[:symbolic_name.index(";")]
        # remove additional information (ie. bundle-version)
        required_bundles[:] = [requiredBundle[:requiredBundle.index(
            ";")] if ";" in requiredBundle else requiredBundle for requiredBundle in required_bundles]
        return symbolic_name, version, exported_packages, imported_packages, required_bundles

    def _trim(self, str):
        return str.replace("\n", "").replace("\r", "").strip(" ")

    def _splitEntries(self, entry, entryName):
        return re.split(r",(?!\d)", entry.replace(entryName, ""))
