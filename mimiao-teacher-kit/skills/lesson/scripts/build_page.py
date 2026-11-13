#!/usr/bin/env python3
"""Build a self-contained HTML player from a Mimiao Teacher Kit package.

Usage: python build_page.py <package.json> [out.html]

The package is validated first; an invalid package writes nothing and exits 1.
Standard library only.
"""
from __future__ import annotations

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from validate_package import load_package, validate  # noqa: E402

TEMPLATE = os.path.join(HERE, "..", "templates", "player.html")
DATA_MARKER = '<script id="kit-data" type="application/json">{}</script>'
TITLE_MARKER = "<title>Mimiao Teacher Kit</title>"
LANG_MARKER = '<html lang="uk">'


def default_output(source: str) -> str:
    for suffix in (".mimiao.json", ".json"):
        if source.endswith(suffix):
            return source[: -len(suffix)] + ".html"
    return source + ".html"


def build_html(template: str, package: dict) -> str:
    """Inject the package into the template; raises KeyError when a marker is missing."""
    for marker in (DATA_MARKER, TITLE_MARKER, LANG_MARKER):
        if template.count(marker) != 1:
            raise KeyError(marker)
    data = json.dumps(package, ensure_ascii=False).replace("</", "<\\/")
    locale = package.get("locale", "uk")
    # str.replace never interprets backslashes in the replacement text.
    page = template.replace(DATA_MARKER, f'<script id="kit-data" type="application/json">{data}</script>')
    page = page.replace(TITLE_MARKER, f"<title>{html.escape(package['title'])}</title>")
    return page.replace(LANG_MARKER, f'<html lang="{locale}">')


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page
        except (AttributeError, ValueError):
            pass
    if len(argv) not in (2, 3):
        print("usage: python build_page.py <package.json> [out.html]", file=sys.stderr)
        return 2
    source = argv[1]
    output = argv[2] if len(argv) == 3 else default_output(source)
    try:
        package = load_package(source)
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"JSON error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"cannot read {source}: {exc}", file=sys.stderr)
        return 2
    errors = validate(package)
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    try:
        with open(TEMPLATE, encoding="utf-8") as handle:
            template = handle.read()
    except OSError as exc:
        print(f"cannot read the player template: {exc}", file=sys.stderr)
        return 2
    try:
        page = build_html(template, package)
    except KeyError as exc:
        print(f"template marker not found exactly once: {exc.args[0]}", file=sys.stderr)
        return 2
    with open(output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(page)
    print(f"page: {output} ({os.path.getsize(output) // 1024 + 1} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
