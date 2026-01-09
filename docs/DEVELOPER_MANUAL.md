**Developer Manual — Pedro Alcàcer website**

**Purpose**: A compact guide to understand, run, edit and deploy this Hugo site so you can manage it independently.

**Prerequisites**
- **Hugo**: Install and verify with `hugo version`. Use Hugo Extended if you need SCSS processing. On macOS: `brew install hugo`.
- **Git**: Site content and history are stored in Git; use `git` to commit/push changes.
- **Optional tools**: `rsync`, `scp`, or CI/CD (GitHub Actions) for deployment.

**Quick snapshot**
- **Site generator**: Hugo (config in [hugo.toml](hugo.toml)).
- **Theme**: `themes/pedroalcacer/` (theme files live there). To customize, override templates in [layouts/](layouts/).
- **Content**: Multilingual content under `content/` (en, es, ca, de, fr, it). See [hugo.toml](hugo.toml) for language settings.
- **Outputs**: `public/` is the generated site (do not edit directly).

**Repository layout (key paths)**
- **`content/`**: All site pages, structured by language (e.g., `content/en/biography/`).
- **`layouts/`**: Project-level templates that override the theme. Create files here to customize output.
- **`themes/pedroalcacer/`**: Theme templates, partials, assets, and shortcodes.
- **`assets/`**: Source assets processed by Hugo Pipes (SCSS, source images for processing).
- **`static/`**: Files copied verbatim to the site root (favicons, static images, downloads).
- **`archetypes/`**: Default front matter templates for new content (see `archetypes/default.md`).
- **`data/`**: Structured data used in templates (JSON/YAML/TOML).
- **`docs/`**: Project documentation (this file is here).
- **`public/`**: Generated output after running `hugo`.
- **`hugo.toml`**: Main Hugo configuration (languages, menus, site params).

**Run the site locally**
- Start the dev server (auto-reloads):

  `hugo server -D`

  - `-D` includes drafts. The server runs at `http://localhost:1313` by default.
- Check Hugo version: `hugo version`.
- Build a production version: `hugo` (output to `public/`).

**Editing content**
- Files are Markdown with front matter (TOML/YAML/JSON). Example front matter keys: `title`, `date`, `draft`, `description`, `type`, `tags`, `menu`.
- Create content for a language under the matching folder, e.g., add `content/en/contact/_index.md` or `content/es/biography/_index.md`.
- Use `archetypes/default.md` to start new pages with sensible defaults.
- Menus are defined in `hugo.toml` per language. To change menu labels or order, edit the `languages.*.menu` blocks.

**Translations / Multilingual notes**
- Each language has its own content directory (see [hugo.toml](hugo.toml)).
- To link pages across languages, use the `translations` front matter or matching filenames and `aliases` where appropriate.
- Hugo will use language-specific templates when placed under `layouts/<LANG>/` or by checking page language in templates.

**Templates & theme customization**
- Override theme templates by adding files with the same path under `layouts/`. Hugo prefers `layouts/` over `themes/...`.
- Key theme files to inspect/edit: `themes/pedroalcacer/layouts/_default/baseof.html`, `single.html`, `list.html`, and any partials under `themes/pedroalcacer/layouts/partials/`.
- Shortcodes live in `layouts/shortcodes/` or `themes/pedroalcacer/layouts/shortcodes/` and are used in content as `{{< shortcode >}}`.
- To change CSS: check `assets/` and theme styles. If the theme uses SCSS and Hugo Pipes, edit SCSS in theme or `assets/` and rebuild with `hugo`.

**Images and media**
- Source images are in `assets/images/` or `static/images/`. Large originals may be stored in `assets/programs/originals/`.
- Prefer Hugo image processing (`.Resources.Get` + `Resize`/`Fit`) in page bundles for responsive images.
- See [docs/instrument-image-optimization.md](docs/instrument-image-optimization.md) for workflows and examples.

**Adding a new page (typical workflow)**
1. Create file in correct language folder, e.g., `content/en/programs/my-program.md`.
2. Add front matter (use `archetypes/default.md` as template).
3. Add images to the page bundle folder (`content/en/programs/my-program/`), or reference from `static/`.
4. Run `hugo server -D` and verify locally.
5. Commit changes and push to the remote repository.

**Deploying the site**
- Generate the site: run `hugo` which writes the static site to `public/`.
- Deployment methods:
  - Push `public/` to a `gh-pages` branch (GitHub Pages), or use a CI pipeline such as GitHub Actions to build and deploy automatically.
  - Copy `public/` to a webserver with `rsync` or `scp`:

    `hugo && rsync -av public/ user@server:/path/to/site/`

- There's a `CNAME` file in the repo and in `static/` — keep it in place for custom domain configuration.

**Backups & large files**
- Keep content tracked in Git; avoid committing very large media to the main repo. Use external storage (S3, CDN) for very large files.
- If you must remove large blobs from Git history, use `git filter-repo` or `git filter-branch` carefully (this rewrites history).

**Troubleshooting**
- Styles not updating: stop the dev server and run `hugo server -D --disableFastRender`.
- Image changes not appearing: clear Hugo cache by removing `resources/_gen/` and rerun the server.
- Missing page refs: `hugo.toml` includes `ignoreErrors = ["error-missing-page-ref"]` to suppress some cross-language reference errors.
- If builds fail, run `hugo --verbose` to get more details.

**Tips & conventions used in this repo**
- Multilingual content is organized by language subdirectories under `content/` (see [hugo.toml](hugo.toml)).
- Use `draft: true` in front matter for pages you don't want published yet.
- Keep translations parallel across language directories for easier cross-linking.
- Edit templates in `layouts/` before touching `themes/pedroalcacer/` unless you want to change the theme globally.

**Where to look next (useful files)**
- Main config: [hugo.toml](hugo.toml)
- Theme: [themes/pedroalcacer/](themes/pedroalcacer/)
- Archetypes: [archetypes/default.md](archetypes/default.md)
- Shortcodes: [layouts/shortcodes/](layouts/shortcodes/)
- This manual: [docs/DEVELOPER_MANUAL.md](docs/DEVELOPER_MANUAL.md)

**Quick how-to: Making common changes (short answers)**
- **Change a menu label or order:** Edit the `languages.<lang>.menu` block in `hugo.toml` and restart the server. Example: change the `name` or `weight` for the menu item.
- **Edit the homepage content:** Check `layouts/index.html` first (project-level); if not present, edit the theme file at `themes/pedroalcacer/layouts/index.html` or the partials it uses (look under `layouts/partials/`).
- **Update a page (e.g., Biography):** Edit the Markdown file under `content/<lang>/biography/` (for example `content/en/biography/_index.md`). Save, then preview with `hugo server -D`.
- **Change a template used by posts/pages:** Edit `layouts/_default/single.html` or the corresponding theme template at `themes/pedroalcacer/layouts/_default/single.html`.
- **Change site styles (CSS/SCSS):** Look in `assets/` and in the theme's assets (e.g., `themes/pedroalcacer/assets/`) for SCSS; otherwise edit `static/css/style.css` if present. After edits, rebuild or use the dev server to preview.
- **Add or update an image for a page:** Put the image in the page bundle next to the page `index.md` (e.g., `content/en/programs/my-program/image.jpg`) and reference it as `![alt text](image.jpg)` or use Hugo image shortcodes/processing in templates.
- **Add a new translated page:** Copy the source file to the corresponding language folder (keep filenames consistent), translate the content, and update front matter. Example: copy `content/en/contact/_index.md` → `content/es/contact/_index.md` and translate.
- **Add or edit a shortcode:** Shortcodes live in `layouts/shortcodes/` or `themes/pedroalcacer/layouts/shortcodes/`. Edit or add a file there and use `{{< name >}}` in Markdown.
- **Test changes locally:** Run `hugo server -D` and open `http://localhost:1313`.
- **Publish changes:** Commit your edits with `git add . && git commit -m "Describe change" && git push`. Then run `hugo` and deploy the `public/` folder via your chosen method (CI, `rsync`, or pushing to a branch).

**If you want, I can next:**
- Add a short checklist for creating a new translated page.
- Create a CI config (GitHub Actions) to build and deploy automatically.

-- End of manual
