Overview: publish a Google Sheet and let a GitHub Action fetch it, convert CSV to JSON and update the site.

Quick steps:

- Create a sheet with the same columns as your CSV (Data;Ciudad;Lugar;Ensemble;Nombre del programa)
- In Google Sheets: File → Publish to the web → choose the sheet and publish as CSV
- From the published sheet URL extract the sheet ID and `gid` (if needed)
- Add repository secrets:
  - `SHEET_ID` — the ID from the sheet URL
  - `SHEET_GID` — the gid number (optional; use `0` if single sheet)
- Trigger the workflow `Update concerts from Google Sheet` (Actions tab) or wait for the nightly run.

Notes:

- The action runs `scripts/tools/fetch_sheet_and_convert.py` which downloads the CSV to `temp_migration/concerts.csv` and calls the converter.
- The converter writes `data/concerts.json` which Hugo loads as `site.Data.concerts`.
- If you prefer YAML, I can change the converter to produce `data/concerts.yaml`.

Security:

- `SHEET_ID` and `SHEET_GID` are stored as repository secrets. If your sheet must be private, you'll need a server-side fetch with credentials; otherwise publishing to the web works fine.

Setup (detailed)

1. Prepare the Google Sheet with the same column order used previously: `Data;Ciudad;Lugar;Ensemble;Nombre del programa`.
2. In Google Sheets: File → Publish to the web → select the sheet and publish as CSV.
3. Copy the published URL and extract the `SHEET_ID` and `gid` values.
4. In your repository Settings → Secrets, add two secrets:
   - `SHEET_ID` — the sheet ID string
   - `SHEET_GID` — the gid integer (use `0` if single tab)
5. Run the workflow manually from Actions → Update concerts from Google Sheet, or wait for the scheduled run.

Files added

- `scripts/tools/fetch_sheet_and_convert.py` — downloads CSV and runs the existing converter.
- `.github/workflows/update-concerts.yml` — scheduled/manual workflow that updates `data/concerts.json`.

Next steps you can ask for

- Switch the converter to output YAML instead of JSON.
- Add a page that lists upcoming concerts only (e.g. filter future dates).
- Add a one-click run guide for non-technical admins.
