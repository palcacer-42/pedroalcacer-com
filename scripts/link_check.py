#!/usr/bin/env python3
"""Simple external link checker for HTML files under public/.
Usage: python scripts/link_check.py
"""
import sys
import os
import re
from urllib.parse import urlparse

try:
    import requests
except Exception:
    print("Missing 'requests' package. Install with: pip install -r requirements.txt")
    sys.exit(2)

ROOT = os.path.join(os.getcwd(), "public")
if not os.path.isdir(ROOT):
    print("public/ not found — run hugo first")
    sys.exit(1)

href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

errors = []
count = 0
for dirpath, _, filenames in os.walk(ROOT):
    for fname in filenames:
        if not fname.lower().endswith('.html'):
            continue
        path = os.path.join(dirpath, fname)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        for m in href_re.finditer(data):
            href = m.group(1)
            if href.startswith('#'):
                continue
            parsed = urlparse(href)
            if parsed.scheme in ('http', 'https'):
                count += 1
                try:
                    r = requests.head(href, allow_redirects=True, timeout=6)
                    status = r.status_code
                except Exception as e:
                    errors.append((href, str(e)))
                    continue
                if status >= 400:
                    errors.append((href, f"HTTP {status}"))

print(f"Checked {count} external links.")
if errors:
    print("Found broken links:")
    for href, why in errors[:50]:
        print(f" - {href}: {why}")
    sys.exit(1)
print("No broken external links found.")
