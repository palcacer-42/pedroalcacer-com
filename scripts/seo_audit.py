#!/usr/bin/env python3
"""Simple local SEO audit for static `public/` HTML files.

Usage: python3 scripts/seo_audit.py

Scans for titles, meta descriptions, canonicals, hreflang alternates,
Open Graph tags, and image alt attributes. Produces a short report.
"""
import os
import re
from collections import defaultdict
from html import unescape

ROOT = "public"

def read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        with open(path, "r", encoding="latin-1") as f:
            return f.read()

def extract(regex, text, flags=re.I|re.S):
    m = re.search(regex, text, flags)
    if not m:
        return None
    # return first non-None capture group
    for i in range(1, len(m.groups())+1):
        g = m.group(i)
        if g:
            return unescape(g.strip())
    return None

def findall(regex, text, flags=re.I|re.S):
    return re.findall(regex, text, flags)

def analyze_file(path):
    txt = read(path)
    title = extract(r"<title[^>]*>(.*?)</title>", txt)
    # allow attributes to be quoted or unquoted
    meta_desc = extract(r'<meta[^>]+name\s*=\s*(?:"description"|\'description\'|description)[^>]*content\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    robots = extract(r'<meta[^>]+name\s*=\s*(?:"robots"|\'robots\'|robots)[^>]*content\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    canonical = extract(r'<link[^>]+rel\s*=\s*(?:"canonical"|\'canonical\'|canonical)[^>]*href\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    og_title = extract(r'<meta[^>]+property\s*=\s*(?:"og:title"|\'og:title\'|og:title)[^>]*content\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    og_desc = extract(r'<meta[^>]+property\s*=\s*(?:"og:description"|\'og:description\'|og:description)[^>]*content\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    alternates = findall(r'<link[^>]+rel\s*=\s*(?:"alternate"|\'alternate\'|alternate)[^>]*hreflang\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))[^>]*href\s*=\s*(?:"(.*?)"|\'(.*?)\'|([^\s>]+))', txt)
    imgs = findall(r'<img\b([^>]*)>', txt)
    img_no_alt = 0
    for attrs in imgs:
        # match alt attribute with optional quotes and non-empty value
        if not re.search(r'\balt\s*=\s*(?:"\s*[^"\']+"|\'\s*[^"\']+\'|[^\s>]+)', attrs, re.I):
            img_no_alt += 1

    return {
        "path": path,
        "title": title,
        "meta_desc": meta_desc,
        "robots": robots,
        "canonical": canonical,
        "og_title": og_title,
        "og_desc": og_desc,
        "alternates": alternates,
        "img_count": len(imgs),
        "img_missing_alt": img_no_alt,
    }

def find_html_files(root):
    out = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith('.html'):
                out.append(os.path.join(dirpath, f))
    return sorted(out)

def main():
    files = find_html_files(ROOT)
    if not files:
        print('No HTML files found under public/. Run your Hugo build first.')
        return

    print(f'Scanning {len(files)} HTML files under {ROOT}/')
    results = [analyze_file(p) for p in files]

    missing_meta = [r for r in results if not r['meta_desc']]
    missing_title = [r for r in results if not r['title']]
    missing_canonical = [r for r in results if not r['canonical']]
    missing_og = [r for r in results if not (r['og_title'] or r['og_desc'])]
    total_imgs = sum(r['img_count'] for r in results)
    total_img_missing = sum(r['img_missing_alt'] for r in results)

    title_map = defaultdict(list)
    for r in results:
        if r['title']:
            title_map[r['title']].append(r['path'])

    duplicate_titles = {t: p for t, p in title_map.items() if len(p) > 1}

    print('\nSummary:')
    print(f'- Pages scanned: {len(files)}')
    print(f'- Pages missing meta description: {len(missing_meta)}')
    print(f'- Pages missing title tag: {len(missing_title)}')
    print(f'- Pages missing canonical tag: {len(missing_canonical)}')
    print(f'- Pages missing OG tags (title/description): {len(missing_og)}')
    print(f'- Total images: {total_imgs} (missing alt: {total_img_missing})')
    print(f'- Duplicate titles found: {len(duplicate_titles)}')

    sitemap = os.path.join(ROOT, 'sitemap.xml')
    robots = os.path.join(ROOT, 'robots.txt')
    print('\nFiles:')
    print(f'- sitemap.xml present: {os.path.exists(sitemap)}')
    print(f'- robots.txt present: {os.path.exists(robots)}')

    if missing_meta:
        print('\nPages missing meta description (examples):')
        for r in missing_meta[:10]:
            print('-', r['path'])

    if missing_title:
        print('\nPages missing title tag (examples):')
        for r in missing_title[:10]:
            print('-', r['path'])

    if duplicate_titles:
        print('\nDuplicate titles (examples):')
        for t, paths in list(duplicate_titles.items())[:10]:
            print('-', repr(t), '->', ', '.join(paths[:4]))

    if total_img_missing:
        print('\nImages missing alt attribute (examples):')
        for r in results:
            if r['img_missing_alt']:
                print(f"- {r['path']} (missing {r['img_missing_alt']})")
                # limit examples
                total_img_missing -= r['img_missing_alt']
                if total_img_missing <= 0:
                    break

    print('\nHreflang alternates present (sample):')
    for r in results[:20]:
        if r['alternates']:
            pairs = []
            for match in r['alternates'][:10]:
                # match may contain multiple groups; pick first non-empty for hreflang and href
                hl = next((x for x in match[0:3] if x), '')
                href = next((x for x in match[3:6] if x), '')
                if hl and href:
                    pairs.append(f"{hl}:{href}")
            if pairs:
                print('-', r['path'], '->', ', '.join(pairs[:5]))

    print('\nDone. Use this report to prioritize metadata, canonical, hreflang and image alt fixes.')

if __name__ == '__main__':
    main()
