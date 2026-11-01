#!/usr/bin/env python3
"""Build the site into a target folder (standard library only).

Steps: render build/content/**/*.html through build/templates/base.html,
write sitemap.xml and robots.txt, copy assets/ and .nojekyll, then run
tools/add_jsonld.py on the result.

Content file format: header lines "key: value" (title, description, noindex,
optional sitemap order), a line "---", then the HTML placed inside <main>.

Usage: python3 build/build.py TARGET_DIR
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = "https://kamgangharold-ui.github.io/tonsite-beaute/"
LASTMOD = "2026-10-24"
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


def sitemap(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for _, path in sorted(entries):
        lines.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{LASTMOD}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build(target):
    target = Path(target)
    base = (HERE / "templates" / "base.html").read_text(encoding="utf-8")
    pages, entries = [], []
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
        if "sitemap" in meta:
            entries.append((int(meta["sitemap"]), path))
    (target / "sitemap.xml").write_bytes(sitemap(entries).encode("utf-8"))
    for f in (HERE / "static").iterdir():
        shutil.copyfile(f, target / f.name)
    (target / ".nojekyll").touch()
    # assets/ stays at the repository root (binary files, css and js are edited in place)
    if (target / "assets").resolve() != ROOT / "assets":
        shutil.copytree(ROOT / "assets", target / "assets", dirs_exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "add_jsonld.py"), str(target)],
                   check=True, stdout=subprocess.DEVNULL)
    return pages


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"built {len(build(sys.argv[1]))} pages into {sys.argv[1]}")
