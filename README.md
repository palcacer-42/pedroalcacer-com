# Pedro Alcàcer - Personal Website

A multi-language Hugo-based static site for Pedro Alcàcer's musician portfolio, hosted on GitHub Pages.

## Overview

This site replaces your previous site with a free, fast, and maintainable alternative built with Hugo static site generator.

**Languages Supported:** English, Spanish (Español), Catalan (Català), German (Deutsch), French (Français), Italian (Italiano)

## Project Guidelines for AI-Assisted Development

These core principles must be followed when working with AI assistance on this project:

1. **Source of Truth**: All content must be based on the original site and HTTrack backup files. These are the authoritative sources for all text, information, images, and structure.

2. **No AI-Generated Content**: All text and information must be sourced from the original site. Do not use AI to fill in missing content, create placeholder text, or generate new descriptions. If content is missing, it must be sourced from the original site or left blank.

3. **Simplicity First**: The structure and implementation strategies must be as simple and understandable as possible. This allows the project owner to:
   - Follow the project logic independently
   - Make modifications without extensive technical knowledge
   - Understand decisions made during development
   - Maintain the site in the future

4. **Document All Decisions**: Every important structural or architectural decision must be documented in this README file. This includes:
   - Why certain approaches were chosen
   - How different sections are organized
   - What alternatives were considered
   - How to modify or extend functionality

These guidelines ensure the project remains maintainable, authentic, and accessible for future work.

## Features

- ✅ **Multi-language support** - 6 languages with automatic navigation
- ✅ **Static & Fast** - Generates plain HTML (no database needed)
- ✅ **SEO Friendly** - Automatic sitemaps and proper meta tags
- ✅ **Responsive Design** - Mobile-friendly out of the box
- ✅ **Free Hosting** - GitHub Pages (no cost)
- ✅ **Easy to Edit** - Simple markdown files for content

<!-- Force deploy trigger: 2026-01-10 -->
- ✅ **Custom Domain** - Use your existing pedroalcacer.com domain
- ✅ **Media Section** - Video previews for performances with YouTube/Vimeo embeds
- ✅ **Instruments Section** - Showcase of early music instruments with builder details

## Project Structure

```
pedroalcacer-site/
├── content/              # Page content (organized by language)
│   ├── en/              # English pages
│   ├── es/              # Spanish pages
│   ├── ca/              # Catalan pages
│   ├── de/              # German pages
│   ├── fr/              # French pages
│   └── it/              # Italian pages
├── themes/
│   └── pedroalcacer/    # Custom theme
│       ├── layouts/     # HTML templates
│       └── static/      # CSS, images, etc.
├── i18n/                # Translation strings
├── hugo.toml            # Main configuration
├── .github/workflows/   # GitHub Actions deployment
└── public/              # Generated website (build output)
```

## Layout Override Strategy

This project uses Hugo's layout override system with layouts in two locations:

- **`/themes/pedroalcacer/layouts/`** - Default theme layouts (12 files)
  - Base templates (`baseof.html`, `index.html`)
  - Section-specific layouts (`biography/`, `contact/`, `discs/`, etc.)
  - Partials and shortcodes

- **`/layouts/`** - Custom layout overrides (8 files)
  - Override theme layouts when you need custom behavior
  - Hugo automatically uses these instead of theme layouts with the same path
  - Examples: custom homepage, specific section modifications

**When to use each:**
- Modify `/themes/pedroalcacer/layouts/` for general theme improvements
- Add to `/layouts/` when you want to override without modifying the theme
- This allows theme updates while preserving custom modifications

## Getting Started Locally

### Prerequisites

- Hugo 0.121.2 or later (already installed)
- Git

### Local Development

1. **Clone the repository** (when you push to GitHub):
```bash
git clone https://github.com/yourusername/pedroalcacer-site.git
cd pedroalcacer-site
```

2. **Start the development server**:
```bash
hugo server
```

3. **Visit** `http://localhost:1313` in your browser

Changes to content files will automatically reload!

## Adding/Editing Content

### Editing an Existing Page

All content is in the `content/` directory. Edit the `.md` (Markdown) files:

```
content/
├── en/biography/_index.md
├── en/instruments/_index.md
├── en/discs/_index.md
├── en/media/_index.md
├── en/programs/_index.md
└── en/contact/_index.md
```

Example - Edit `content/en/biography/_index.md`:
```markdown
---
title: "Biography"
description: "Learn about Pedro Alcàcer"
---

## About Pedro Alcàcer

Your content here...
```

### Adding a New Page

1. Create a new file in the appropriate language folder
2. Add frontmatter (title, etc.)
3. Write your content in Markdown

Example creating a new projects page:
```bash
mkdir -p content/en/projects
cat > content/en/projects/_index.md << 'EOF'
---
title: "Projects"
description: "My projects"
---

## Recent Projects

Content here...
EOF
```

Then add to menu in `hugo.toml`:
```toml
[[menu.main]]
  name = "Projects"
  url = "/projects/"
  weight = 8
```

### Translating to Other Languages

1. Copy the English `.md` file to each language folder
2. Update the content in that language

Example for Spanish biography:
```bash
cp content/en/biography/_index.md content/es/biography/_index.md
# Edit content/es/biography/_index.md with Spanish translation
```

## Images & Media

Place images in `themes/pedroalcacer/static/images/`:

Reference in Markdown:
```markdown
![Description]({{ "images/photo.jpg" | relURL }})
```

### Media Section

The media section displays video previews for performances. Videos are embedded from YouTube and Vimeo.

**Structure:**
- Content defined in `content/*/media/_index.md` frontmatter under `media` array
- Each item has `title`, `artist`, and optional `video_url`
- Layout in `layouts/section/media.html` renders a responsive grid
- CSS styles in `public/css/style.css` for `.media-grid`, `.media-item`, etc.

**Adding Videos:**
1. Add to the `media` array in each language's `_index.md`
2. Include `video_url` for YouTube/Vimeo links
3. Items without `video_url` show "Video coming soon" placeholder

Example:
```yaml
media:
  - title: "Piece Title"
    artist: "Artist Name"
    video_url: "https://www.youtube.com/watch?v=VIDEO_ID"
```

The layout automatically detects YouTube/Vimeo and embeds appropriately.

## Configuration

Main settings in `hugo.toml`:

- **baseURL** - Your website domain
- **title** - Site title
- **defaultContentLanguage** - Default language (en)
- **[languages]** - Language definitions
- **[menu.main]** - Navigation menu items

## Navigation & responsiveness

- The header uses a simple, dependency-free hamburger toggle on screens ≤1024px. The checkbox with `#nav-toggle` drives the show/hide state for the `.nav-block` that contains both the main menu and the language selector.
- Menu items wrap as whole items; no words should break mid-link. On mobile, the menu and language links stack vertically to maximize above-the-fold space.
- Cache busting for CSS is handled via the `?v=YYYYMMDD` query on `css/style.css` in the base layout. Update this version string if you need to force browsers to fetch new styles after changes.

## Building for Production

```bash
hugo  # Creates /public directory
```

The `public/` folder contains the complete static website ready to deploy.

## Deployment to GitHub Pages

### Step 1: Initialize Git Repository

```bash
cd pedroalcacer-site
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `pedroalcacer-site`
3. Choose **Public** (required for free GitHub Pages)
4. **DO NOT** initialize with README (you already have files)

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/yourusername/pedroalcacer-site.git
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - **Source:** GitHub Actions
   - The workflow file (`.github/workflows/deploy.yml`) will auto-deploy

### Step 5: Point Your Domain

In your domain registrar (where you bought pedroalcacer.com):

1. Find **DNS settings**
2. Add **CNAME record**:
   - Name: `www`
   - Value: `yourusername.github.io`

Or for root domain:
   - Add **A records** pointing to GitHub's IP addresses:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```

3. In GitHub repository Settings → Pages → "Custom domain": `pedroalcacer.com`

**Wait 10-24 hours for DNS to propagate**

## Translations

UI strings (buttons, labels) are in `i18n/` directory:

- `i18n/en.toml` - English
- `i18n/es.toml` - Spanish
- `i18n/ca.toml` - Catalan
- `i18n/de.toml` - German
- `i18n/fr.toml` - French
- `i18n/it.toml` - Italian

Example in `i18n/en.toml`:
```toml
learn_more = "Learn More"
read_more = "Read More"
```

Use in templates:
```html
{{ i18n "learn_more" }}
```

## Customization

### Change Colors

Edit `themes/pedroalcacer/static/css/style.css`:

```css
:root {
    --primary-color: #2c3e50;      /* Dark blue */
    --accent-color: #e74c3c;        /* Red accent */
    --text-color: #333;
    --bg-color: #fff;
    /* ... */
}
```

### Change Logo/Branding

Edit `themes/pedroalcacer/layouts/baseof.html` - the navbar section:

```html
<div class="nav-brand">
    <a href="{{ .Site.BaseURL }}{{ .Lang }}/">Pedro Alcàcer</a>
</div>
```

### Add Social Links

Edit footer in `themes/pedroalcacer/layouts/baseof.html`:

```html
<div class="social-links">
    <a href="YOUR_FACEBOOK_URL" target="_blank">
        <i class="fab fa-facebook"></i>
    </a>
    <!-- Add more links -->
</div>
```

## Troubleshooting

### Site builds but pages show "404"

- Check `baseURL` in `hugo.toml` matches your domain
- Ensure content is in `content/en/`, `content/es/`, etc.

### Language switching not working

- Verify all 6 languages in `hugo.toml` have corresponding `i18n/XX.toml` files
- Check content exists in language folders

### Changes not showing up

- Run `hugo` to rebuild
- Clear browser cache (Ctrl+Shift+Delete)
- Delete `/public` and rebuild: `rm -rf public && hugo`

### GitHub Pages not updating

- Check **Actions** tab in GitHub repository for build errors
- Verify `.github/workflows/deploy.yml` exists
- Ensure repository is **Public**

## Future Enhancements

Possible additions:
- [ ] Blog section with dates
- [ ] Image galleries for performances
- [ ] Contact form integration (Netlify Forms, Formspree)
- [ ] Newsletter signup
- [ ] Event calendar
- [ ] PDF downloads (sheet music, CV)
- [ ] Search functionality

## Support & Resources

- **Hugo Documentation:** https://gohugo.io/documentation/
- **GitHub Pages Help:** https://docs.github.com/en/pages
- **Markdown Guide:** https://www.markdownguide.org/

## License

Content: © 2026 Pedro Alcàcer
Theme: MIT License

---

**Your website is now ready to deploy! Next steps:**
1. Initialize Git and push to GitHub
2. Enable GitHub Pages in settings
3. Add your custom domain
4. Start adding your content!

## Development Log

### January 8, 2026

*   **Programs Section Completed:** Fully developed the Programs section across all 6 languages (English, Spanish, Catalan, German, French, Italian) with comprehensive content including:
    *   Solo Programs: Detailed descriptions for 5 concert programs (Bologna liutística, Tres territorios, Dos peninsulas, Una storia fra le corde, Tanyer de gala)
    *   Ensemble Programs: Complete ensemble member listings for 6 groups (Anima Shirvani, Caravelle della musica, Viaggio musicale nell'Emilia del 600', Volcania, Arlecchino innamorato, Les musiques du Roi Soleil)
    *   Separate pages for solo and ensemble programs with navigation
    *   All content based on original site data, following project guidelines

### January 7, 2026

*   **Homepage Links Fixed:** Corrected all navigation links on the homepage, including the main call-to-action buttons, the primary navigation menu, and the language switcher. The links now correctly navigate within the selected language.
*   **Simplified Code:** Refactored the layout templates (`baseof.html`, `index.html`) for simplicity and easier future maintenance, following best practices.
*   **Project Documentation:** Initialized this `README.md` file to document the project structure, setup, and progress.

## Album Links Shortcode

You can render an elegant, data-driven album card with platform links using the `album_links` shortcode.

- Data file location: `data/albums/<id>.yaml` (example: `data/albums/luis-milan.yaml`).
- Shortcode usage in any content page:

```html
{{< album_links id="luis-milan" >}}
```

- Supported link keys: `spotify`, `deezer`, `tidal`, `bandcamp`, `youtube`, `amazon`.
- Optional keys: `cover` (URL or site path), `year`.

Example `data/albums/luis-milan.yaml`:

```yaml
title: "Luis Milán: El Maestro"
year: 2025
cover: "/images/albums/luis-milan-cover.jpg"
links:
    spotify: "https://open.spotify.com/album/1B2TgPuNXzNFRmfzthtYer"
    deezer:  "https://www.deezer.com/album/664086261"
    tidal:   "https://listen.tidal.com/album/396979243"
    bandcamp: "https://palcacer.bandcamp.com/album/..."
    youtube: "https://www.youtube.com/playlist?list=..."
    amazon:  "https://music.amazon.it/…"
```

Notes:
- Place album cover images under `themes/pedroalcacer/static/images/albums/` or a public `static/` path and reference via `cover`.
- The shortcode injects SVG icons for each platform (you can swap icons in `layouts/shortcodes/album_links.html`).
- Styles are in `themes/pedroalcacer/static/css/style.css` under the `.album-card` and `.album-link-button` rules.

## Concerts CSV → JSON converter

To avoid Hugo parsing errors with semicolon CSVs, the project includes a small converter that outputs `data/concerts.json` used by the site.

- Script: `scripts/tools/convert_concerts.py` — converts a semicolon-separated CSV to JSON compatible with Hugo.
- Fetcher (optional): `scripts/tools/fetch_sheet_and_convert.py` — downloads a published Google Sheet as CSV and invokes the converter.
- GitHub Action: `.github/workflows/update-concerts.yml` can be used to run the fetch/convert on a schedule or manually.

Usage (local):

```bash
python3 scripts/tools/convert_concerts.py temp_migration/concerts.csv data/concerts.json
# or to fetch a published sheet first
python3 scripts/tools/fetch_sheet_and_convert.py <SHEET_ID>
```

If you prefer keeping the Google Sheet private, consider the documented Apps Script push option in `docs/google-apps-script/`.

## Icons and Styling

- Platform icons are embedded SVGs inside `layouts/shortcodes/album_links.html` and given a circular subtle background via CSS.
- To use official brand marks, replace the inline SVGs with licensed SVG files stored in `themes/pedroalcacer/static/icons/` and adjust the shortcode.

## Adding a new album page

1. Create the data file: `data/albums/<id>.yaml`.
2. Create localized content pages: `content/<lang>/discs/<id>/index.md` and include the shortcode.
3. Rebuild the site: `hugo` or run `hugo server -D` for live preview.


---
