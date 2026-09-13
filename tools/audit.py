#!/usr/bin/env python
"""Audit the static demo against the same claims used in the sales pitch."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
BASE = "https://twenion.github.io/manufacturing-site-demo/"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.h1: list[str] = []
        self.title: list[str] = []
        self.descriptions: list[str] = []
        self.canonicals: list[str] = []
        self.og: dict[str, str] = {}
        self.images: list[dict[str, str | None]] = []
        self.links: list[str] = []
        self.assets: list[str] = []
        self.json_ld: list[str] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._svg_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "svg":
            self._svg_depth += 1
        if tag == "html":
            self.html_lang = data.get("lang") or ""
        if tag == "h1" or (tag == "title" and self._svg_depth == 0):
            self._capture = tag
            self._buffer = []
        if tag == "script" and data.get("type") == "application/ld+json":
            self._capture = "json"
            self._buffer = []
        if tag == "meta" and data.get("name", "").lower() == "description":
            self.descriptions.append(data.get("content") or "")
        if tag == "meta" and (data.get("property") or "").startswith("og:"):
            self.og[data["property"]] = data.get("content") or ""
        if tag == "link" and "canonical" in (data.get("rel") or "").split():
            self.canonicals.append(data.get("href") or "")
        if tag == "img":
            self.images.append(data)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag in {"img", "script", "source"} and data.get("src"):
            self.assets.append(data["src"])
        if tag == "link" and data.get("href") and "stylesheet" in (data.get("rel") or "").split():
            self.assets.append(data["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg":
            self._svg_depth = max(0, self._svg_depth - 1)
            return
        expected = {"h1": "h1", "title": "title", "script": "json"}.get(tag)
        if expected is None or self._capture != expected:
            return
        value = " ".join("".join(self._buffer).split())
        if expected == "h1":
            self.h1.append(value)
        elif expected == "title":
            self.title.append(value)
        else:
            self.json_ld.append(value)
        self._capture = None
        self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)


def empty_value(value: object) -> bool:
    if value is None or value == "":
        return True
    if isinstance(value, dict):
        return any(empty_value(item) for item in value.values())
    if isinstance(value, list):
        return not value or any(empty_value(item) for item in value)
    return False


def local_target(page: Path, reference: str) -> Path | None:
    clean = unquote(reference.split("#", 1)[0].split("?", 1)[0])
    if not clean or clean.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
        return None
    if clean.startswith("/"):
        return page.parent / clean.lstrip("/")
    return page.parent / clean


def audit(root: Path = ROOT) -> list[str]:
    faults: list[str] = []
    pages = sorted(root.glob("*.html"))
    if not pages:
        return ["site: no HTML pages found"]

    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    expected_sitemap: set[str] = set()
    required_og = {"og:type", "og:locale", "og:title", "og:description", "og:url", "og:site_name"}

    for page in pages:
        parser = PageParser()
        text = page.read_text(encoding="utf-8")
        parser.feed(text)
        name = page.name
        is_404 = name == "404.html"

        if parser.html_lang != "az":
            faults.append(f"{name}: html lang must be az")
        if len(parser.h1) != 1 or not parser.h1[0]:
            faults.append(f"{name}: expected exactly one non-empty h1")
        if len(parser.title) != 1 or not 20 <= len(parser.title[0]) <= 75:
            faults.append(f"{name}: title missing or outside 20-75 characters")
        elif not is_404:
            if parser.title[0] in titles:
                faults.append(f"{name}: title duplicates {titles[parser.title[0]]}")
            titles[parser.title[0]] = name
        if len(parser.descriptions) != 1 or not 70 <= len(parser.descriptions[0]) <= 180:
            faults.append(f"{name}: meta description missing or outside 70-180 characters")
        elif not is_404:
            if parser.descriptions[0] in descriptions:
                faults.append(f"{name}: description duplicates {descriptions[parser.descriptions[0]]}")
            descriptions[parser.descriptions[0]] = name

        if not is_404:
            expected = BASE if name == "index.html" else BASE + name
            if parser.canonicals != [expected]:
                faults.append(f"{name}: canonical does not match {expected}")
            if missing := required_og - parser.og.keys():
                faults.append(f"{name}: missing Open Graph fields {sorted(missing)}")
            if parser.og.get("og:url") != expected:
                faults.append(f"{name}: og:url does not match canonical")
            if not parser.json_ld:
                faults.append(f"{name}: JSON-LD missing")
            for index, block in enumerate(parser.json_ld, 1):
                try:
                    data = json.loads(block)
                except json.JSONDecodeError as error:
                    faults.append(f"{name}: JSON-LD {index} invalid ({error.msg})")
                    continue
                if empty_value(data):
                    faults.append(f"{name}: JSON-LD {index} contains an empty field")
            expected_sitemap.add(expected)

        for image in parser.images:
            if image.get("alt") is None:
                faults.append(f"{name}: image missing alt")
            if image.get("alt") == "" and "aria-hidden" not in image:
                faults.append(f"{name}: decorative image missing aria-hidden")
        for href in parser.links:
            if href.startswith("mail:"):
                faults.append(f"{name}: invalid mail: protocol")
            target = local_target(page, href)
            if target is not None and not target.exists():
                faults.append(f"{name}: broken link {href}")
        for src in parser.assets:
            if src.startswith(("http://", "https://")):
                faults.append(f"{name}: third-party runtime asset {src}")
            target = local_target(page, src)
            if target is not None and not target.exists():
                faults.append(f"{name}: missing asset {src}")
        searchable = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", text, flags=re.I | re.S)
        searchable = re.sub(r"<[^>]+>", " ", searchable)
        if re.search(r"\b(lorem ipsum|todo|tbd|placeholder|salam dünya)\b", searchable, re.I):
            faults.append(f"{name}: placeholder text found")

    robots = root / "robots.txt"
    sitemap = root / "sitemap.xml"
    if not robots.exists():
        faults.append("site: robots.txt missing")
    elif f"Sitemap: {BASE}sitemap.xml" not in robots.read_text(encoding="utf-8"):
        faults.append("site: robots.txt sitemap URL is wrong")
    if not sitemap.exists():
        faults.append("site: sitemap.xml missing")
    else:
        try:
            tree = ET.parse(sitemap)
            found = {node.text or "" for node in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
            if found != expected_sitemap:
                missing = sorted(expected_sitemap - found)
                extra = sorted(found - expected_sitemap)
                faults.append(f"site: sitemap mismatch missing={missing} extra={extra}")
        except ET.ParseError as error:
            faults.append(f"site: sitemap XML invalid ({error})")

    return faults


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    faults = audit(root)
    if faults:
        print(f"AUDIT FAILED — {len(faults)} fault(s)")
        for fault in faults:
            print(f"- {fault}")
        return 1
    print(f"AUDIT PASSED — {len(list(root.glob('*.html')))} pages, 0 faults")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
