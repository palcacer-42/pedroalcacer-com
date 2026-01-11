#!/usr/bin/env python3
import re
import os

PUBLIC_DIR = os.path.join(os.getcwd(), 'public')
# Prefer a language page that contains the client script (use default language page)
INDEX_HTML = os.path.join(PUBLIC_DIR, 'en', 'index.html')

with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r"var supportedLangs\s*=\s*\[([^\]]*)\]", html)
if not m:
    print('Could not find supportedLangs in public/index.html')
    exit(1)

langs_raw = m.group(1)
# extract strings
supported = re.findall(r'"([a-zA-Z-]+)"', langs_raw)
supported = [s.split('-')[0].lower() for s in supported]

m2 = re.search(r'var fallbackLang\s*=\s*"([^"]+)"', html)
fallback = m2.group(1) if m2 else 'en'

print('Supported languages:', supported)
print('Fallback language:', fallback)

paths_to_test = ['/', '/programs/', '/discs/luis-milan/']

test_lang_lists = [
    ['es-ES', 'es'],
    ['ca-ES', 'ca'],
    ['de-DE', 'de'],
    ['it-IT', 'it'],
    ['fr-FR', 'fr'],
    ['zh-CN', 'zh'],
    ['en-US', 'en'],
    []
]


def pick_lang(user_langs, supported):
    for tag in user_langs:
        tag = (tag or '').lower()
        if not tag:
            continue
        if tag in supported:
            return tag
        primary = tag.split('-')[0]
        if primary in supported:
            return primary
    return None


def build_target(pathname, lang):
    if pathname == '/' or pathname == '':
        return '/' + lang + '/'
    p = pathname if pathname.startswith('/') else ('/' + pathname)
    return '/' + lang + (p if p != '/' else '/')


def exists_target(target):
    # target like '/es/' or '/es/programs/' or '/es/discs/luis-milan/'
    t = target.lstrip('/')
    if target.endswith('/'):
        candidate = os.path.join(PUBLIC_DIR, t, 'index.html')
        return os.path.exists(candidate), candidate
    else:
        candidate = os.path.join(PUBLIC_DIR, t)
        return os.path.exists(candidate), candidate

for langs in test_lang_lists:
    print('\nUser navigator.languages =', langs)
    for path in paths_to_test:
        chosen = pick_lang(langs, supported) or fallback
        target = build_target(path, chosen)
        ok, cand = exists_target(target)
        if ok:
            print(f'  Path {path} -> redirect to {target} (exists: {cand})')
        else:
            fb_target = build_target(path, fallback)
            ok2, cand2 = exists_target(fb_target)
            print(f'  Path {path} -> chosen {chosen} not found; fallback to {fb_target} (exists: {ok2 and cand2 or "missing"})')

print('\nDone')
