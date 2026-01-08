#!/usr/bin/env python3
"""Fetch a Google Sheet CSV export and convert it to Hugo data.

Usage:
  python3 scripts/tools/fetch_sheet_and_convert.py --sheet-id SHEET_ID [--gid GID]

Environment fallback: SHEET_ID and SHEET_GID env vars are supported.
The script writes to `temp_migration/concerts.csv` and then runs
`scripts/tools/convert_concerts.py` to produce `data/concerts.json`.
"""
from pathlib import Path
import argparse
import os
import sys
import urllib.request
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT_CSV = ROOT / 'temp_migration' / 'concerts.csv'


def fetch_csv(sheet_id: str, gid: str | None):
    gid_param = f"&gid={gid}" if gid else ""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv{gid_param}"
    print(f"Fetching CSV from: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "concerts-sync/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.write_bytes(data)
    print(f"Wrote CSV to {OUT_CSV}")


def run_converter():
    script = ROOT / 'scripts' / 'tools' / 'convert_concerts.py'
    if not script.exists():
        print(f"Converter not found: {script}")
        sys.exit(1)
    print("Running converter...")
    subprocess.run([sys.executable, str(script)], check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sheet-id', help='Google Sheet ID', default=os.environ.get('SHEET_ID'))
    p.add_argument('--gid', help='Sheet gid (optional)', default=os.environ.get('SHEET_GID'))
    args = p.parse_args()
    if not args.sheet_id:
        print('Sheet ID is required (use --sheet-id or $SHEET_ID)')
        sys.exit(2)
    fetch_csv(args.sheet_id, args.gid)
    run_converter()


if __name__ == '__main__':
    main()
