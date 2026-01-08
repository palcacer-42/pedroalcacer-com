#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

ROOT = Path.cwd()
INFILE = ROOT / 'temp_migration' / 'concerts.csv'
OUTFILE = ROOT / 'data' / 'concerts.json'

if not INFILE.exists():
    print(f"Input file not found: {INFILE}")
    sys.exit(1)

with INFILE.open(encoding='utf-8') as fh:
    reader = csv.reader(fh, delimiter=';')
    rows = [r for r in reader]

if not rows:
    print("No rows found in CSV")
    sys.exit(1)

headers = [h.strip() for h in rows[0]]
mapping = {
    'data': 'date',
    'ciudad': 'city',
    'lugar': 'venue',
    'ensemble': 'ensemble',
    'nombre del programa': 'program'
}

records = []
for row in rows[1:]:
    # normalize length
    row = [c.strip() for c in row]
    if len(row) < len(headers):
        row += [''] * (len(headers) - len(row))
    rec = {}
    for h, v in zip(headers, row):
        key = h.lower().strip()
        key = mapping.get(key, key.replace(' ', '_'))
        rec[key] = v
    records.append(rec)

OUTFILE.parent.mkdir(parents=True, exist_ok=True)
with OUTFILE.open('w', encoding='utf-8') as fh:
    json.dump(records, fh, ensure_ascii=False, indent=2)

print(f"Wrote {OUTFILE} ({len(records)} records)")
