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
    reader = csv.reader(fh, delimiter=',')
    rows = [r for r in reader]

if not rows:
    print("No rows found in CSV")
    sys.exit(1)

# Find header row
header_idx = -1
for i, row in enumerate(rows):
    # Check for keywords in row to identify header
    row_str = "".join(row).lower()
    if "data" in row_str and "ciudad" in row_str:
        header_idx = i
        break

if header_idx == -1:
    print("Could not find header row (looking for 'Data', 'Ciudad')")
    # Fallback to 0 if not found, though likely wrong
    header_idx = 0

print(f"Found headers at row {header_idx}: {rows[header_idx]}")
headers = [h.strip() for h in rows[header_idx]]

# Filter out empty headers (like the first empty col)
# We will use the index of non-empty headers to map values
valid_indices = [i for i, h in enumerate(headers) if h]
valid_headers = [headers[i] for i in valid_indices]

mapping = {
    'data': 'date',
    'ciudad': 'city',
    'lugar': 'venue',
    'ensemble': 'ensemble',
    'nombre del programa': 'program'
}

records = []
for row in rows[header_idx+1:]:
    # Skip empty rows
    if not "".join(row).strip():
        continue
        
    # normalize length
    row = [c.strip() for c in row]
    
    rec = {}
    for i, h in zip(valid_indices, valid_headers):
        if i < len(row):
            val = row[i]
            key = h.lower().strip()
            key = mapping.get(key, key.replace(' ', '_'))
            rec[key] = val
    
    # Only add if we have at least a date or program
    if rec.get('date') or rec.get('program'):
        records.append(rec)


OUTFILE.parent.mkdir(parents=True, exist_ok=True)
with OUTFILE.open('w', encoding='utf-8') as fh:
    json.dump(records, fh, ensure_ascii=False, indent=2)

print(f"Wrote {OUTFILE} ({len(records)} records)")
