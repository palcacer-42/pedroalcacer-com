#!/usr/bin/env bash
set -euo pipefail

echo "Running site checks..."

# Build site
echo "Building site with hugo..."
hugo

# Run SEO script if present
if [ -x "scripts/generate_seo_report.py" ] || [ -f "scripts/generate_seo_report.py" ]; then
  echo "Running SEO report script..."
  python3 scripts/generate_seo_report.py || true
fi

# Run link checker
if command -v python3 >/dev/null 2>&1; then
  echo "Running link checker (this may take a while)..."
  python3 scripts/link_check.py
else
  echo "python3 not found; skipping link check"
fi

echo "All checks completed."
