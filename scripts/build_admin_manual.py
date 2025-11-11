#!/usr/bin/env python3
"""
Build a single ADMIN_MANUAL.md by concatenating repository Markdown files.
Creates:
 - docs/admin_manual/ADMIN_MANUAL.md
 - docs/admin_manual/INDEX.md

Usage: python scripts/build_admin_manual.py

The script skips the `docs/admin_manual` folder itself and `.git`.
"""
from pathlib import Path
import datetime
import math
import re

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "admin_manual"
EXCLUDE_DIRS = {".git", "docs/admin_manual", "venv", ".venv", ".venv311", "__pycache__"}

OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 -]", "", s)
    s = s.replace(" ", "-")
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def find_md_files(root: Path):
    files = []
    for p in root.rglob("*.md"):
        if is_excluded(p.relative_to(root)):
            # also skip the output dir if present
            continue
        # skip the main README.md in repo root only if you want -- we'll include it
        files.append(p)
    files = sorted(files, key=lambda p: (str(p.parent), p.name))
    return files


def first_heading(text: str):
    for line in text.splitlines():
        if line.strip().startswith("#"):
            return line.strip().lstrip("# ")
    return None


def chunk_list(lst, n):
    # split into n chunks as evenly as possible
    k, m = divmod(len(lst), n)
    chunks = []
    i = 0
    for j in range(n):
        size = k + (1 if j < m else 0)
        if size:
            chunks.append(lst[i:i+size])
        i += size
    return [c for c in chunks if c]


def build_manual(files):
    total = len(files)
    if total == 0:
        print("No markdown files found to include.")
        return

    # decide number of volumes
    if total > 200:
        volumes = 5
    elif total > 120:
        volumes = 4
    elif total > 60:
        volumes = 3
    elif total > 20:
        volumes = 2
    else:
        volumes = 1

    chunks = chunk_list(files, volumes)

    out_file = OUT_DIR / "ADMIN_MANUAL.md"
    index_file = OUT_DIR / "INDEX.md"

    now = datetime.datetime.utcnow().isoformat() + "Z"

    with out_file.open("w", encoding="utf-8") as out:
        out.write(f"# Admin Manual\n\n")
        out.write(f"_Generated: {now} UTC — contains {total} markdown files from repository._\n\n")
        out.write("---\n\n")

        for vi, chunk in enumerate(chunks, start=1):
            out.write(f"## Volume {vi} — {len(chunk)} files\n\n")
            for fi, p in enumerate(chunk, start=1):
                rel = p.relative_to(ROOT)
                text = p.read_text(encoding="utf-8")
                title = first_heading(text) or p.stem
                anchor = f"volume-{vi}-chapter-{fi}-{slugify(title)}"
                out.write(f"### {title} — `{rel}`\n\n")
                out.write(f"<a name=\"{anchor}\"></a>\n\n")
                out.write(text)
                out.write("\n\n---\n\n")

    # build a simple index.md with links
    with index_file.open("w", encoding="utf-8") as idx:
        idx.write("# Admin Manual Index\n\n")
        idx.write(f"_Generated: {now} UTC — {total} files, {volumes} volumes._\n\n")
        for vi, chunk in enumerate(chunks, start=1):
            idx.write(f"## Volume {vi}\n\n")
            for fi, p in enumerate(chunk, start=1):
                rel = p.relative_to(ROOT)
                text = p.read_text(encoding="utf-8")
                title = first_heading(text) or p.stem
                anchor = f"volume-{vi}-chapter-{fi}-{slugify(title)}"
                idx.write(f"- [{title} — `{rel}`](./ADMIN_MANUAL.md#{anchor})\n")
            idx.write("\n")

    print(f"Wrote {out_file} and {index_file} — {total} files into {len(chunks)} volume(s).")


if __name__ == "__main__":
    files = find_md_files(ROOT)
    build_manual(files)
