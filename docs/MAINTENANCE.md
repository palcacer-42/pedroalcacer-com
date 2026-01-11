# Site Maintenance & Checklist

This document complements `docs/DEVELOPER_MANUAL.md` with short, repeatable steps to keep the Hugo site healthy.

## Quick checklist (per change)

- Preview locally:

```bash
hugo server -D
# open http://localhost:1313 and verify changed pages
```

- Build production output:

```bash
hugo
# inspect public/ for expected output
```

- Run repository checks:
  - Search for broken links / missing page refs in changed pages.
  - Run the SEO script (if present): `python scripts/generate_seo_report.py`.

- Image & media checks:
  - Ensure images referenced from `content/*` exist under `static/images/` or as page-bundle resources.
  - Use short, hyphenated filenames: `vanitas-vanitatum.png`.

- Commit discipline:
  - Use feature branches for non-trivial edits:

```bash
git checkout -b feat/short-description
```

  - Make small, focused commits and push to origin for PRs.

- Pull requests & review:
  - Open a PR for template/major content changes. Include preview links.
  - Rely on CI preview builds to validate rendering across languages.

## CI & Deployment

- Pin the Hugo version in CI to match local tests.
- CI should build the site, run the SEO script and a basic link-checker before deploying.
- Typical deploy flows:
  - GitHub Actions build → Netlify/Vercel deploy (use previews for PRs).
  - Manual: run `hugo` and `rsync`/`scp` the `public/` folder.

## Rollback plan

- To revert a bad deploy, `git revert <commit>` and re-deploy.
- Use host UI (Netlify/Vercel) to roll back to the previous successful deploy when available.

## Backups & large media

- Avoid committing very large media to Git; store large archives externally (S3, GDrive) and reference them.
- Periodically archive the repository or mirror to a backup location.

## Updating dependencies

- Python:

```bash
pip install -r requirements.txt --upgrade
```

- Node/npm:

```bash
npm install
npm audit fix
```

Test scripts after upgrades before committing.

## Periodic checks (monthly or per-release)

- Verify translations are present across language folders.
- Run `hugo` and visually scan major site sections.
- Run and act on the SEO report.

## Contacts & secrets

- Put deploy keys and API tokens in CI secrets (GitHub Actions secrets, Netlify env vars). Never commit secrets.

---

If you want, I can add a small `scripts/checksite.sh` that runs `hugo`, the SEO report, and a link-checker. I can also wire it into a GitHub Actions workflow to run on PRs.
