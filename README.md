# DIMSONSGFX — Digital Creative Assets Portfolio

🌐 **Live Website:** [https://dimsonsgfx.github.io](https://dimsonsgfx.github.io)  
📦 **GitHub Repository:** [https://github.com/dimsonsgfx/dimsonsgfx.github.io](https://github.com/dimsonsgfx/dimsonsgfx.github.io)

Modern, fast, fully responsive static portfolio hosted on **GitHub Pages**, styled after the **Simple Blog v2 (avaxgfxgreen)** design system:
- **English UI and Content:** English navigation, titles, descriptions, and metadata
- **Clean 3-Column Grid:** Post cards rendered in 3 columns for optimal desktop viewing
- **Simplified Sidebar:** Only the Categories block in the left sidebar (extra blocks removed)
- **Brand Emblem & Logo:** Custom circular glowing emblem (`logo-icon.png`) + `DIMSONSGFX` typography
- **New Favicon:** High-resolution multi-format favicon (`favicon.png`, `favicon.ico`, `apple-touch-icon`)
- **No Views Counter:** Views count icon removed from all short cards and single item pages
- **5 Focused Categories:**
  1. 🖨️ **3D Print Models** (`/category/3d-print-models/`)
  2. 📊 **PowerPoint Templates** (`/category/powerpoint-templates/`)
  3. 📄 **InDesign Templates** (`/category/indesign-templates/`)
  4. 💻 **Mockup Templates** (`/category/mockup-templates/`)
  5. 🎨 **UI Design Kits** (`/category/ui-design-kits/`)
- **Dark & Light Mode:** Toggleable theme with zero-flash initial loading and `localStorage` persistence
- **Full SEO Suite:** Schema.org JSON-LD (`WebSite`, `Person`, `BreadcrumbList`, `ImageObject`, `CreativeWork`), Open Graph, Twitter Cards, XML Image Sitemap, and `robots.txt`

---

## Quick Start (Build & Deploy)

The site is built with a self-contained Python generator with zero external pip dependencies.

1. Rebuild all HTML, category archives, work pages, and sitemaps:
```bash
python scripts/build.py
```
2. Deploy to GitHub Pages:
```bash
git add -A
git commit -m "Update portfolio items"
git push
```
GitHub Pages automatically deploys the updated `main` branch in ~1-2 minutes.

---

## File Structure

```text
dimsonsgfx.github.io/
├── index.html              ← Homepage (Latest Works + All Works)
├── 404.html                ← 404 Error page (noindex)
├── sitemap.xml             ← XML Sitemap with image:image metadata
├── robots.txt              ← Search engine crawler rules
├── .nojekyll               ← Prevents GitHub Pages Jekyll processing
├── category/               ← Category archive pages with pagination
│   ├── 3d-print-models/
│   ├── powerpoint-templates/
│   ├── indesign-templates/
│   ├── mockup-templates/
│   └── ui-design-kits/
├── works/                  ← Single item detail pages
│   ├── cyberpunk-helmet-mk4/
│   ├── pitch-deck-pro-presentation/
│   └── ...
├── search/                 ← Fast client-side search
│   └── index.html
├── assets/
│   ├── css/
│   │   ├── styles.css      ← Base template stylesheet
│   │   ├── patch.css       ← 3-column grid, dark theme, logo styles
│   │   └── fonts.css       ← Font Awesome declarations
│   ├── js/
│   │   ├── libs.js         ← Core template scripts
│   │   └── site.js         ← Theme switcher, mobile drawer, search
│   ├── images/             ← Work preview cards, favicon.png, logo-icon.png
│   ├── dleimages/          ← UI icons
│   └── webfonts/           ← Font Awesome 5 Pro fonts
├── data/
│   ├── works.json          ← Complete database of portfolio items
│   └── categories.json     ← Category metadata and icons
└── scripts/
    └── build.py            ← Static site generation script
```

---

## How to Add a New Item

All items are stored in [`data/works.json`](data/works.json).

### 1. Prepare your preview image
- Save file using **Latin letters and hyphens** (e.g. `cyber-helmet-3d.webp` or `pitch-deck-preview.jpg`, NOT `IMG_1234.jpg`).
- Place the image in `assets/images/`.

### 2. Add an entry to `data/works.json`:
```json
{
  "slug": "futuristic-mech-drone",
  "title": "Futuristic Mech Drone 3D Print",
  "description": "Articulated mechanical drone designed for FDM and SLA 3D printing. Features movable ball joints, high-resolution panel lining, and pre-supported STL files. Perfect for tabletop wargaming and collectors.",
  "category": "3d-print-models",
  "categoryLabel": "3D Print Models",
  "date": "2026-10-05",
  "image": "/assets/images/futuristic-mech-drone.webp",
  "thumb": "/assets/images/futuristic-mech-drone.webp",
  "emoji": "🤖",
  "tags": ["3D Print", "Mecha", "STL", "Miniature"],
  "views": 0,
  "source": "manual"
}
```

### 3. Rebuild and publish:
```bash
python scripts/build.py
git add -A && git commit -m "Add Futuristic Mech Drone" && git push
```

---

## Search Console & Webmaster Verification

In [`scripts/build.py`](scripts/build.py), verification code variables are ready:

```python
GOOGLE_VERIFICATION = ""   # Paste Google Search Console verification code here
YANDEX_VERIFICATION = ""   # Paste Yandex Webmaster verification code here
```

### Google Search Console Setup
1. Go to [Google Search Console](https://search.google.com/search-console/).
2. Select **URL prefix** and enter: `https://dimsonsgfx.github.io`
3. Choose the **HTML tag** verification method.
4. Copy the `content` code string.
5. In `scripts/build.py`, set:
   ```python
   GOOGLE_VERIFICATION = "YOUR_CODE_HERE"
   ```
6. Run `python scripts/build.py`, commit and push to GitHub.
7. Click **Verify** in Google Search Console.
8. Go to **Sitemaps** and submit: `https://dimsonsgfx.github.io/sitemap.xml`

### Yandex Webmaster Setup
1. Go to [Yandex Webmaster](https://webmaster.yandex.com/).
2. Add site: `https://dimsonsgfx.github.io`
3. Select **Meta tag** verification.
4. Copy the code from `content` attribute.
5. In `scripts/build.py`, set:
   ```python
   YANDEX_VERIFICATION = "YOUR_CODE_HERE"
   ```
6. Run `python scripts/build.py`, commit and push.
7. Click **Check** in Yandex Webmaster.
8. Submit Sitemap URL: `https://dimsonsgfx.github.io/sitemap.xml`

---

## Telegram Autoposting Architecture

The project is structured to easily integrate an automated poster from a Telegram channel via GitHub Actions:

### 1. Channel Post Format
```text
Item Name

Full description of the item in 2-3 detailed sentences. Specify software used, key features, and file formats included.

#3dprint #stl #design
```

### 2. Hashtag Category Mapping
- `#3dprint`, `#3dmodels`, `#stl` → `3d-print-models`
- `#powerpoint`, `#presentation`, `#pitchdeck` → `powerpoint-templates`
- `#indesign`, `#editorial`, `#magazine` → `indesign-templates`
- `#mockup`, `#psd`, `#branding` → `mockup-templates`
- `#uikit`, `#figma`, `#ui` → `ui-design-kits`

### 3. Automated GitHub Action Workflow
`.github/workflows/telegram-sync.yml` can poll new Telegram channel media via Telegram Bot API, compress images to WebP (85%), append new objects to `data/works.json`, run `python scripts/build.py`, and push directly to `main`.

---

## Implemented Features

- [x] Full English localization
- [x] Custom favicon & circular brand emblem
- [x] Removed views counter from short cards and single item pages
- [x] Simplified sidebar: removed "Editor's Pick" and "Top Works", keeping ONLY Categories
- [x] Responsive 3-column layout (avaxgfxgreen style)
- [x] Dark / Light theme toggle with `localStorage`
- [x] Instant client-side search over JSON database
- [x] Schema.org JSON-LD (`WebSite`, `Person`, `BreadcrumbList`, `ImageObject`, `CreativeWork`)
- [x] XML Sitemap with `<image:image>` extension
- [x] `robots.txt` configuration
- [x] GitHub Pages hosting at `https://dimsonsgfx.github.io`
