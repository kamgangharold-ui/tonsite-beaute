---
name: web-design-guidelines
description: "Checklist review of UI source files against the Vercel Web Interface Guidelines (accessibility, focus, forms, performance, i18n), reported as file and line findings. Use for requests to review UI code, audit accessibility of files, or check against best practices. Not for visual direction."
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Read the pinned guidelines in `command.md` next to this file (do not fetch anything from the network)
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in `command.md`
4. Output findings in the terse `file:line` format

## Guidelines Source

`command.md` is a pinned copy of the Vercel Web Interface Guidelines, read and approved on 2026-10-25:
repository vercel-labs/web-interface-guidelines, commit 434b7f91364665f2f733b310ec54809bf8f37937,
sha256 d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234. The original skill fetched
this file live from the main branch before each review; that was replaced by this local copy so the
rules cannot change without a review. To update, re-read the new file, then replace `command.md` and
the hash in SOURCE.md.

Two project overrides for French sites: use sentence case for headings and buttons (ignore
the Title Case rule), and keep autofill on forms (ignore the `autocomplete="off"` rule for non auth fields).

## Usage

When a user provides a file or pattern argument:
1. Read `command.md`
2. Read the specified files
3. Apply all rules from `command.md`
4. Output findings using the format specified in `command.md`

If no files specified, ask the user which files to review.
