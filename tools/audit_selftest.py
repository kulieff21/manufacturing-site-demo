#!/usr/bin/env python
"""Inject representative defects and prove the audit reports each one."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from audit import ROOT, audit


CASES = {
    "wrong language": ("index.html", 'lang="az"', 'lang="en"', "html lang"),
    "missing h1": ("index.html", "<h1", "<h2", "exactly one non-empty h1"),
    "invalid email protocol": ("index.html", "mailto:", "mail:", "invalid mail: protocol"),
    "broken internal link": ("index.html", 'href="imkanlar.html"', 'href="yoxdur.html"', "broken link"),
    "remote runtime asset": ("index.html", 'src="assets/js/site.js"', 'src="https://cdn.example/site.js"', "third-party runtime asset"),
    "placeholder copy": ("index.html", "Bu sayt portfolio", "TODO Bu sayt portfolio", "placeholder text"),
    "invalid JSON-LD": ("index.html", '"@context": "https://schema.org"', '"@context": ', "JSON-LD"),
    "wrong canonical": ("materiallar.html", "materiallar.html\"", "material.html\"", "canonical"),
    "missing description": ("keyfiyyet.html", '<meta name="description"', '<meta name="x-description"', "meta description"),
}


def main() -> int:
    baseline = audit(ROOT)
    if baseline:
        print("Baseline must pass before self-test:")
        print("\n".join(f"- {fault}" for fault in baseline))
        return 1

    passed = 0
    for label, (filename, old, new, expected) in CASES.items():
        with tempfile.TemporaryDirectory(prefix="kesim-audit-") as temp:
            copy = Path(temp) / "site"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "_screenshots", "__pycache__"))
            path = copy / filename
            content = path.read_text(encoding="utf-8")
            if old not in content:
                print(f"FAIL {label}: injection target missing")
                continue
            path.write_text(content.replace(old, new, 1), encoding="utf-8")
            faults = audit(copy)
            if any(expected in fault for fault in faults):
                print(f"PASS {label}")
                passed += 1
            else:
                print(f"FAIL {label}: expected {expected!r}, got {faults}")
    print(f"SELF-TEST — {passed}/{len(CASES)} injected faults caught")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
