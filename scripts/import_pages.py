#!/usr/bin/env python3
"""Import static HTML pages into Jinja templates that extend shell.html.

Usage:
  python scripts/import_pages.py --src pages_to_import --dst templates/pages --dry-run

This script will:
- Read all .html files from --src
- Extract <head> and <body>
- Create templates at --dst/<slug>.html with:
    {% extends 'shell.html' %}
    {% block page_title %}...{% endblock %}
    {% block head_extra %}...{% endblock %}
    {% block content %}...{% endblock %}
- Backup originals to --dst/originals/

Notes:
- This is a best-effort converter. Manual fixes are expected for pages with complex head scripts or relative asset paths.
"""
from pathlib import Path
import argparse
from bs4 import BeautifulSoup
import shutil
from pathlib import PurePosixPath
import shutil


def convert_file(src_path: Path, dst_dir: Path, backup_dir: Path, extract_head=True, static_dest: Path = Path('static/pages'), copy_assets: bool = True):
    html = src_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head
    body = soup.body

    if body is None:
        content_html = html
    else:
        content_html = ''.join(str(x) for x in body.contents)

    head_html = ''
    if extract_head and head is not None:
        # remove title (we'll set a nicer one) but keep meta and scripts
        # keep everything except <title>
        head_children = [c for c in head.contents if getattr(c, 'name', None) != 'title']
        head_html = ''.join(str(x) for x in head_children).strip()

    slug = src_path.stem
    # Rewrite local asset paths like <img src="images/foo.png"> or <link href="styles.css">
    # and copy assets to static_dest/<slug>/...
    def _is_remote(path: str) -> bool:
        s = (path or '').strip()
        return s.startswith('http://') or s.startswith('https://') or s.startswith('//') or s.startswith('/') or s.startswith('data:') or s.startswith('#')

    if static_dest and (head is not None or body is not None):
        for tag_name, attr in [('img', 'src'), ('script', 'src'), ('link', 'href'), ('source', 'src'), ('video', 'src'), ('audio', 'src')]:
            for el in soup.find_all(tag_name):
                if not el.has_attr(attr):
                    continue
                val = el.get(attr)
                if not val:
                    continue
                if _is_remote(val):
                    continue
                # strip query/hash
                asset_rel = val.split('?', 1)[0].split('#', 1)[0]
                asset_src = (src_path.parent / asset_rel).resolve()
                if not asset_src.exists() or not asset_src.is_file():
                    continue
                dest_asset = static_dest / slug / asset_rel
                dest_asset.parent.mkdir(parents=True, exist_ok=True)
                if copy_assets:
                    shutil.copy2(asset_src, dest_asset)
                # update attribute to use the site static path
                web_path = PurePosixPath(static_dest.as_posix()) / slug / PurePosixPath(asset_rel)
                el[attr] = '/' + str(web_path)

        # update head_html as we will re-extract it later
        if head is not None:
            head_children = [c for c in head.contents if getattr(c, 'name', None) != 'title']
            head_html = ''.join(str(x) for x in head_children).strip()

    # slug already set above
    out_path = dst_dir / f"{slug}.html"

    template = []
    template.append("{% extends 'shell.html' %}\n")
    template.append("{% block page_title %}\n")
    template.append(slug.replace('_', ' ').title() + "\n")
    template.append("{% endblock %}\n\n")
    if head_html:
        template.append("{% block head_extra %}\n")
        template.append(head_html + "\n")
        template.append("{% endblock %}\n\n")
    template.append("{% block content %}\n")
    template.append(content_html + "\n")
    template.append("{% endblock %}\n")

    backup_dir.mkdir(parents=True, exist_ok=True)
    dst_dir.mkdir(parents=True, exist_ok=True)

    # write backup and template
    shutil.copy2(src_path, backup_dir / src_path.name)
    out_path.write_text(''.join(template), encoding='utf-8')
    return out_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--src', default='pages_to_import')
    p.add_argument('--dst', default='templates/pages')
    p.add_argument('--static-dest', default='static/pages', help='Where to copy page-local static assets (images, css, etc.)')
    p.add_argument('--no-copy-assets', action='store_true', help='Do not copy local assets; just rewrite paths')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--sample', type=int, default=5, help='How many files to convert in dry-run')
    args = p.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    backup = dst / 'originals'

    if not src.exists():
        print(f'Source directory {src} does not exist. Create it and put your HTML files there.')
        return

    files = sorted(src.glob('*.html'))
    if not files:
        print(f'No HTML files found in {src}')
        return

    to_process = files[:args.sample] if args.dry_run else files
    print(f'Processing {len(to_process)} files (dry_run={args.dry_run})')
    for f in to_process:
        out = convert_file(f, dst, backup, static_dest=Path(args.static_dest), copy_assets=not args.no_copy_assets)
    print(f'Converted {f.name} -> {out}')

if __name__ == '__main__':
    main()
