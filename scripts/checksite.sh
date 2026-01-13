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

echo "All checks completed."
