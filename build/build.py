#!/usr/bin/env python3
"""Build the site into a target folder. Standard library only.

Usage: python3 build/build.py TARGET_DIR
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROBOTS_LINE = '<meta name="robots" content="noindex">'


def read_content(path):
    head, sep, body = path.read_text(encoding="utf-8").partition("\n---\n")
    if not sep:
        raise ValueError(f"{path}: missing '---' separator")
    meta = {}
    for line in head.splitlines():
        key, _, value = line.partition(": ")
        meta[key] = value
    return meta, body


def build(target):
    target = Path(target)
    base = (HERE / "templates" / "base.html").read_text(encoding="utf-8")
    pages = []
    for src in sorted((HERE / "content").rglob("*.html")):
        rel = src.relative_to(HERE / "content")
        meta, body = read_content(src)
        prefix = "../" * (len(rel.parts) - 1)
        path = "" if rel.as_posix() == "index.html" else rel.as_posix()
        html = base
        for key, value in (
            ("{{robots_line}}", ROBOTS_LINE if meta["noindex"] == "yes" else ""),
            ("{{title}}", meta["title"]),
            ("{{description}}", meta["description"]),
            ("{{prefix}}", prefix),
            ("{{path}}", path),
            ("{{body}}", body),
        ):
            html = html.replace(key, value)
        out = target / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(html.encode("utf-8"))
        pages.append(rel.as_posix())
    for f in (HERE / "static").iterdir():
        shutil.copyfile(f, target / f.name)
    (target / ".nojekyll").touch()
    # assets/ stays at the repository root (binary files and css/js are edited in place)
    if target.resolve() != ROOT:
        shutil.copytree(ROOT / "assets", target / "assets", dirs_exist_ok=True)
    return pages


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"built {len(build(sys.argv[1]))} pages into {sys.argv[1]}")
