#!/usr/bin/env python3
"""Build claude-plugin/dist/mimiao-teacher-kit.zip (reproducible).

Validates every skills/lesson/examples/*.mimiao.json first; any error aborts the build.
Standard library only.
"""
from __future__ import annotations

import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(ROOT, "mimiao-teacher-kit")
DIST_DIR = os.path.join(ROOT, "dist")
ZIP_PATH = os.path.join(DIST_DIR, "mimiao-teacher-kit.zip")
EXAMPLES_DIR = os.path.join(PLUGIN_DIR, "skills", "lesson", "examples")
FIXED_TIME = (1980, 1, 1, 0, 0, 0)

sys.path.insert(0, os.path.join(PLUGIN_DIR, "skills", "lesson", "scripts"))
from validate_package import load_package, validate  # noqa: E402


def validate_examples() -> list[str]:
    problems: list[str] = []
    for name in sorted(os.listdir(EXAMPLES_DIR)):
        if not name.endswith(".mimiao.json"):
            continue
        path = os.path.join(EXAMPLES_DIR, name)
        try:
            errors = validate(load_package(path))
        except (ValueError, OSError) as exc:
            errors = [f"JSON error: {exc}"]
        problems.extend(f"{name}: {line}" for line in errors)
    return problems


def collect_files() -> list[str]:
    found: list[str] = []
    for directory, subdirs, files in os.walk(PLUGIN_DIR):
        subdirs[:] = [d for d in subdirs if d != "__pycache__"]
        for name in files:
            if name.endswith(".pyc") or name == ".DS_Store":
                continue
            full = os.path.join(directory, name)
            found.append(os.path.relpath(full, ROOT).replace(os.sep, "/"))
    return sorted(found)


def main() -> int:
    problems = validate_examples()
    if problems:
        for line in problems:
            print(line, file=sys.stderr)
        return 1
    os.makedirs(DIST_DIR, exist_ok=True)
    files = collect_files()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for rel in files:
            info = zipfile.ZipInfo(rel, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(ROOT, rel), "rb") as handle:
                archive.writestr(info, handle.read())
    print(f"zip: {ZIP_PATH} ({os.path.getsize(ZIP_PATH) // 1024 + 1} KB, {len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
