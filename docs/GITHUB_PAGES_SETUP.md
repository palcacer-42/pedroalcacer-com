# GitHub Pages & DNS setup (quick checklist)

Follow these steps to make GitHub Pages serve your built `public/` site at your custom domain and enable HTTPS.

1) Choose canonical domain
   - Recommended: `pedroalcacer.com` (apex) with `www` redirecting to it.

2) DNS records
   - Apex (`pedroalcacer.com`) — add A records (GitHub Pages):
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - `www` — add a CNAME record pointing to your GitHub Pages target (example):
     - `www` CNAME -> `palcacer-42.github.io`  (replace with your GitHub Pages host)
   - Remove any other conflicting redirects or proxies (Cloudflare, Netlify) during setup.

3) GitHub repository settings → Pages
   - Branch: `gh-pages` or `main` (depending on your chosen deployment method). For user/org pages, choose the published branch.
   - Set Custom domain to `pedroalcacer.com` (or `www.pedroalcacer.com`) and save.
   - After saving, enable **Enforce HTTPS** (GitHub will provision a certificate; may take a few minutes).

4) Verify DNS & propagation
   - Use `dig` to confirm propagation:
```bash
dig +short A pedroalcacer.com
dig +short CNAME www.pedroalcacer.com
```
   - Confirm the site serves your content:
```bash
curl -I -L https://pedroalcacer.com
curl -sS https://pedroalcacer.com/robots.txt
curl -sS https://pedroalcacer.com/sitemap.xml | sed -n '1,40p'
```

5) Common pitfalls
   - A 301 HTML page from an intermediary (nginx) usually indicates a proxy or redirecting host in front of GitHub Pages — remove or reconfigure it.
   - If using Cloudflare, set DNS to `CNAME` (not proxied / orange cloud) until HTTPS is provisioned.

6) After site serves real content
   - Verify `robots.txt` and `sitemap.xml` are served properly.
   - Open Google Search Console and add/verify the property (use `https://pedroalcacer.com/`).
   - Submit `https://pedroalcacer.com/sitemap.xml` in Search Console → Sitemaps and request indexing for important pages.

7) Optional: automate deploy
   - Use GitHub Actions to build Hugo and push `public/` to the publishing branch, or configure GitHub Pages to build from the repository if you prefer.

If you want, I can prepare a branch and PR with these repo changes and a GitHub Actions workflow to build and publish automatically. Should I create that PR now?
