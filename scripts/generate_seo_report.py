#!/usr/bin/env python3
"""Generate CSV-style SEO report from content front matter and public HTML.

Produces three reports in `scripts/reports/`:
- missing_descriptions.csv: path,title
- duplicate_titles.csv: title,paths (| separated)
- images_missing_alt.csv: public_html_path,missing_count
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
CONTENT_DIR = os.path.join(ROOT, 'content')
PUBLIC_DIR = os.path.join(ROOT, 'public')
REPORT_DIR = os.path.join(os.path.dirname(__file__), 'reports')

def ensure_report_dir():
    os.makedirs(REPORT_DIR, exist_ok=True)

def list_content_files():
    exts = ('.md', '.markdown', '.html')
    out = []
    for dirpath, dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.lower().endswith(exts):
                out.append(os.path.join(dirpath, f))
    return sorted(out)

def parse_front_matter(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    fm = None
    s = txt.lstrip()
    if s.startswith('---'):
        parts = s.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
    elif s.startswith('+++'):
        parts = s.split('+++', 2)
        if len(parts) >= 3:
            fm = parts[1]
    if not fm:
        return {}

    # crude extraction for title and description
    title = None
    desc = None
    for line in fm.splitlines():
        m = re.match(r'^title\s*[:=]\s*["\']?(.*?)["\']?\s*$', line.strip(), re.I)
        if m and not title:
            title = m.group(1).strip()
            continue
        m2 = re.match(r'^description\s*[:=]\s*["\']?(.*?)["\']?\s*$', line.strip(), re.I)
        if m2 and not desc:
            desc = m2.group(1).strip()
            continue

    return {'title': title, 'description': desc}

def scan_contents():
    files = list_content_files()
    missing_desc = []
    title_map = defaultdict(list)
    total = 0
    for p in files:
        rel = os.path.relpath(p, ROOT)
        total += 1
        fm = parse_front_matter(p)
        title = fm.get('title') if fm else None
        desc = fm.get('description') if fm else None
        if not desc:
            missing_desc.append((rel, title or ''))
        if title:
            title_map[title].append(rel)

    duplicate_titles = {t: ps for t, ps in title_map.items() if len(ps) > 1}
    return missing_desc, duplicate_titles, total

def scan_public_images():
    out = []
    for dirpath, dirs, files in os.walk(PUBLIC_DIR):
        for f in files:
            if f.lower().endswith('.html'):
                path = os.path.join(dirpath, f)
                with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                    txt = fh.read()
                imgs = re.findall(r'<img\b([^>]*)>', txt, re.I)
                miss = 0
                for attrs in imgs:
                    if not re.search(r'\balt\s*=\s*["\']\s*[^"\']+', attrs, re.I):
                        miss += 1
                if miss:
                    out.append((os.path.relpath(path, ROOT), miss))
    return out

def write_csv_missing(descs):
    p = os.path.join(REPORT_DIR, 'missing_descriptions.csv')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('path,title\n')
        for path, title in descs:
            # escape commas
            t = title.replace(',', ' ') if title else ''
            f.write(f'{path},{t}\n')
    return p

def write_csv_duplicates(dups):
    p = os.path.join(REPORT_DIR, 'duplicate_titles.csv')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('title,paths\n')
        for title, paths in dups.items():
            t = title.replace(',', ' ')
            f.write(f'{t},{"|".join(paths)}\n')
    return p

def write_csv_images(imgs):
    p = os.path.join(REPORT_DIR, 'images_missing_alt.csv')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('public_html_path,missing_count\n')
        for path, miss in imgs:
            f.write(f'{path},{miss}\n')
    return p

def main():
    ensure_report_dir()
    missing_desc, duplicate_titles, total_pages = scan_contents()
    imgs = scan_public_images()
    p1 = write_csv_missing(missing_desc)
    p2 = write_csv_duplicates(duplicate_titles)
    p3 = write_csv_images(imgs)

    print('Report generated:')
    print(f'- content pages scanned: {total_pages}')
    print(f'- missing descriptions: {len(missing_desc)} -> {p1}')
    print(f'- duplicate titles: {len(duplicate_titles)} -> {p2}')
    print(f'- public images missing alt: {len(imgs)} -> {p3}')

if __name__ == "__main__":
    main()
