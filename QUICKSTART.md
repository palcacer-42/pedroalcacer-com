# 🚀 Quick Start Guide - Pedro Alcàcer Website

Your Hugo multi-language website is ready! Here's what you have:

## ✅ What's Installed

- **Hugo Static Site Generator** - Zero maintenance, lightning fast
- **Multi-language Theme** - English, Spanish, Catalan, German, French, Italian
- **GitHub Pages Ready** - Automatic deployment on every push
- **Custom Domain Ready** - Points to your pedroalcacer.com

## 📁 Project Location

```
/home/palcacer/pedroalcacer-site/
```

## 🎯 Next Steps (In Order)

### 1️⃣ **Local Testing** (Optional)
Test the site locally before deploying:

```bash
cd /home/palcacer/pedroalcacer-site
~/.local/bin/hugo server
```
Then visit: `http://localhost:1313`

Press `Ctrl+C` to stop.

### 2️⃣ **Initialize Git**

```bash
cd /home/palcacer/pedroalcacer-site
git init
git add .
git commit -m "Initial Hugo site"
```

### 3️⃣ **Create GitHub Repository**

1. Go to https://github.com/new
2. Repository name: **`pedroalcacer-site`**
3. Choose **PUBLIC** (important!)
4. Do NOT initialize with README
5. Click "Create repository"

### 4️⃣ **Push to GitHub**

Copy the commands shown after creating the repository. Usually:

```bash
cd /home/palcacer/pedroalcacer-site
git remote add origin https://github.com/YOUR_USERNAME/pedroalcacer-site.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 5️⃣ **Enable GitHub Pages**

1. Go to: https://github.com/YOUR_USERNAME/pedroalcacer-site
2. Click **Settings** (top right)
3. Left menu → **Pages**
4. Under "Build and deployment":
   - Source: **GitHub Actions** (should auto-detect)
5. Done! Site will deploy automatically

### 6️⃣ **Set Up Custom Domain** (Optional but Recommended)

#### For `pedroalcacer.com`:/home/palcacer/websites/pedroalcacer.com/

**With your domain registrar** (wherever you bought /home/palcacer/websites/pedroalcacer.com/the domain):
1. Find **DNS settings** 
2. Add **CNAME record**:
   - Name: `www`
   - Value: `YOUR_USERNAME.github.io`

**In GitHub repository**:
1. Settings → Pages
2. "Custom domain": `pedroalcacer.com`
3. ✅ Check "Enforce HTTPS"

DNS can take 10-24 hours to propagate. Check with `nslookup`:
```bash
nslookup pedroalcacer.com
```

## ✏️ Editing Content

All content is in Markdown files:

```
content/en/biography/_index.md
content/en/instruments/_index.md
content/en/discs/_index.md
content/en/media/_index.md
content/en/programs/_index.md
content/en/contact/_index.md
```

### To Update English Pages:
1. Edit the `.md` files in `content/en/`
2. Commit and push to GitHub
3. Site auto-builds in ~1 minute

### To Add Other Languages:
Copy English files to language folders:
```bash
cp -r content/en/* content/es/  # Spanish
cp -r content/en/* content/ca/  # Catalan
# ... etc for de/, fr/, it/
```

Then translate the content.

## 🎨 Customization

**Colors:** Edit `themes/pedroalcacer/static/css/style.css`

**Layout:** Edit `themes/pedroalcacer/layouts/baseof.html`

**Translations:** Edit `i18n/en.toml`, `i18n/es.toml`, etc.

**Menu items:** Edit `hugo.toml`

## 📊 Site Structure

After building, the generated website is in `public/`:

```
public/
├── index.html          (Root page)
├── en/                 (English pages)
├── es/                 (Spanish pages)
├── ca/                 (Catalan pages)
├── de/                 (German pages)
├── fr/                 (French pages)
├── it/                 (Italian pages)
├── css/                (Stylesheets)
└── sitemap.xml
```

## 🔄 Updating After First Deploy

Every time you make changes:

```bash
cd /home/palcacer/pedroalcacer-site
git add .
git commit -m "Update content"
git push
```

GitHub automatically rebuilds and deploys within 1-2 minutes!

## 💡 Useful Commands

```bash
# Build site
cd /home/palcacer/pedroalcacer-site
~/.local/bin/hugo

# Start local dev server
~/.local/bin/hugo server

# Clean build
rm -rf public && ~/.local/bin/hugo

# Check git status
git status

# View recent commits
git log --oneline
```

## ❓ Common Questions

**Q: How do I add images?**
A: Place in `themes/pedroalcacer/static/images/` and reference:
```markdown
![Alt text]({{ "images/myimage.jpg" | relURL }})
```

**Q: Can I use my own domain?**
A: Yes! Follow Step 6 above. Full instructions in README.md

**Q: How do I add a new language?**
A: Create folder in `content/newlang/` and add language in `hugo.toml`

**Q: Is there a cost?**
A: No! Hugo, GitHub, and GitHub Pages are all free.

**Q: Can I use without Git/GitHub?**
A: The `public/` folder has your complete website - you can upload it anywhere (Netlify, etc.)

## 📚 Resources

- **Full Documentation:** See `README.md` in the site folder
- **Hugo Help:** https://gohugo.io/documentation/
- **GitHub Pages:** https://docs.github.com/en/pages
- **Markdown Guide:** https://www.markdownguide.org/

---

## 🎉 You're All Set!

Your professional website is ready to deploy. The site is:
- ✅ Fast (static HTML)
- ✅ Free (GitHub Pages)
- ✅ Professional (responsive design)
- ✅ Multi-language (6 languages)
- ✅ Easy to maintain (simple markdown files)
- ✅ SEO friendly (sitemaps, proper meta tags)

**Now push it to GitHub and show the world your music! 🎵**

