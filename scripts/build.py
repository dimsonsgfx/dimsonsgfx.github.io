#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIMSONSGFX — Build script v3 (English Edition)
Updates:
  - Full English translation across all templates, SEO, and navigation
  - Categories: 3D Print Models, PowerPoint Templates, InDesign Templates, Mockup Templates, UI Design Kits
  - Removed views counter icon from both shortstory cards and fullstory pages
  - Sidebar simplified: removed "Editor's Pick" and "Top Works", keeping ONLY Categories
  - New custom favicon and circular logo badge integration
  - JSON-LD structured data (ImageObject, BreadcrumbList, WebSite, Person)
  - XML Image Sitemap & robots.txt
"""
import json, os
from datetime import datetime

SITE_URL    = "https://dimsonsgfx.github.io"
SITE_NAME   = "DIMSONSGFX"
SITE_AUTHOR = "DIMSONSGFX"
BASE  = r"C:\Users\dimso\dimsonsgfx-site"
DATA  = os.path.join(BASE, "data")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── Webmaster verification codes ────────────────
GOOGLE_VERIFICATION  = ""   # Paste Google Search Console code here
YANDEX_VERIFICATION  = ""   # Paste Yandex Webmaster code here

# ── Helpers ──────────────────────────────────────
def esc(s):
    return str(s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def esc_js(s):
    return str(s or "").replace("\\","\\\\").replace('"','\\"').replace("\n"," ").replace("\r","")

def fmt_date(d):
    if not d: return ""
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        months = ["","January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
        return f"{months[dt.month]} {dt.day}, {dt.year}"
    except:
        return d

def img_alt(w):
    cat = cat_map.get(w.get("category",""), {})
    cat_label = cat.get("label", w.get("category",""))
    return f"{w.get('title','')} - {cat_label}"

def og_image_url(w):
    img = w.get("image","") or w.get("thumb","")
    if img:
        if img.startswith("http"):
            return img
        return f"{SITE_URL}{img}"
    return f"{SITE_URL}/assets/images/og-default.svg"

# ── Webmaster meta tags ────────────────────────
def webmaster_meta():
    tags = []
    if GOOGLE_VERIFICATION:
        tags.append(f'\t<meta name="google-site-verification" content="{esc(GOOGLE_VERIFICATION)}">')
    else:
        tags.append('\t<!-- GOOGLE SEARCH CONSOLE: Add code below or in GOOGLE_VERIFICATION in build.py -->')
        tags.append('\t<!-- <meta name="google-site-verification" content="YOUR_CODE_HERE"> -->')
    if YANDEX_VERIFICATION:
        tags.append(f'\t<meta name="yandex-verification" content="{esc(YANDEX_VERIFICATION)}">')
    else:
        tags.append('\t<!-- YANDEX WEBMASTER: Add code below -->')
        tags.append('\t<!-- <meta name="yandex-verification" content="YOUR_CODE_HERE"> -->')
    return "\n".join(tags)

# ── Theme init ──────────────────────────────────
THEME_INIT = """<script>
(function(){
  var t=localStorage.getItem('dimsonsgfx-theme')||
    (window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
  document.documentElement.setAttribute('data-theme',t);
  document.addEventListener('DOMContentLoaded',function(){
    document.body.setAttribute('data-theme',t);
  });
})();
</script>"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&family=Rubik:wght@300;400;500&display=swap" rel="stylesheet">'

# ── <head> ────────────────────────────────────
def head_html(title, desc, og_img, canonical, schema_ld="", page_type="website"):
    wm = webmaster_meta()
    return f"""<!DOCTYPE html>
<html lang="en">
{THEME_INIT}
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">

\t<!-- Primary SEO -->
\t<title>{esc(title)}</title>
\t<meta name="description" content="{esc(desc)}">
\t<link rel="canonical" href="{esc(canonical)}">
\t<meta name="robots" content="index, follow">

\t<!-- Open Graph / Facebook / Telegram -->
\t<meta property="og:title" content="{esc(title)}">
\t<meta property="og:description" content="{esc(desc)}">
\t<meta property="og:image" content="{esc(og_img)}">
\t<meta property="og:image:width" content="1200">
\t<meta property="og:image:height" content="630">
\t<meta property="og:url" content="{esc(canonical)}">
\t<meta property="og:type" content="{page_type}">
\t<meta property="og:locale" content="en_US">
\t<meta property="og:site_name" content="{esc(SITE_NAME)}">

\t<!-- Twitter Card -->
\t<meta name="twitter:card" content="summary_large_image">
\t<meta name="twitter:title" content="{esc(title)}">
\t<meta name="twitter:description" content="{esc(desc)}">
\t<meta name="twitter:image" content="{esc(og_img)}">

\t<!-- Verification -->
{wm}

\t<!-- Icons & Favicon -->
\t<link rel="shortcut icon" href="/assets/images/favicon.png" type="image/png">
\t<link rel="icon" href="/assets/images/favicon.ico" type="image/x-icon">
\t<link rel="apple-touch-icon" href="/assets/images/logo-icon.png">
\t<meta name="theme-color" content="#36c537">

\t<!-- Fonts & CSS -->
\t{FONTS}
\t<link href="/assets/css/styles.css" type="text/css" rel="stylesheet">
\t<link href="/assets/css/patch.css" type="text/css" rel="stylesheet">

\t<!-- JSON-LD -->
{schema_ld}
</head>"""

# ── JSON-LD helpers ─────────────────────────────
def schema_website():
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebSite",
      "@id": "{SITE_URL}/#website",
      "name": "{esc_js(SITE_NAME)}",
      "url": "{SITE_URL}/",
      "description": "Portfolio of 3D print models, presentation templates, mockups, and UI design kits",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": "{SITE_URL}/search/?q={{search_term_string}}",
        "query-input": "required name=search_term_string"
      }}
    }},
    {{
      "@type": "Person",
      "@id": "{SITE_URL}/#author",
      "name": "{esc_js(SITE_AUTHOR)}",
      "url": "{SITE_URL}/"
    }}
  ]
}}
</script>"""

def schema_work(w, canonical):
    cat = cat_map.get(w.get("category",""), {})
    cat_label = cat.get("label", w.get("category",""))
    img_url = og_image_url(w)
    alt = img_alt(w)
    desc = w.get("description","") or alt

    breadcrumb = f"""{{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Home","item":"{SITE_URL}/"}},
        {{"@type":"ListItem","position":2,"name":"{esc_js(cat_label)}","item":"{SITE_URL}/category/{esc_js(w['category'])}/"}},
        {{"@type":"ListItem","position":3,"name":"{esc_js(w['title'])}","item":"{esc_js(canonical)}"}}
      ]
    }}"""

    image_obj = f"""{{
      "@type": "ImageObject",
      "@id": "{esc_js(canonical)}#image",
      "contentUrl": "{esc_js(img_url)}",
      "name": "{esc_js(alt)}",
      "description": "{esc_js(desc)}",
      "datePublished": "{esc_js(w.get('date',''))}",
      "author": {{"@type":"Person","name":"{esc_js(SITE_AUTHOR)}"}}
    }}"""

    creative_work = f"""{{
      "@type": "CreativeWork",
      "@id": "{esc_js(canonical)}#work",
      "name": "{esc_js(w['title'])}",
      "description": "{esc_js(desc)}",
      "url": "{esc_js(canonical)}",
      "datePublished": "{esc_js(w.get('date',''))}",
      "image": "{esc_js(img_url)}",
      "genre": "{esc_js(cat_label)}",
      "author": {{"@type":"Person","name":"{esc_js(SITE_AUTHOR)}"}}
    }}"""

    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [{breadcrumb},{image_obj},{creative_work}]
}}
</script>"""

def schema_category(cat, canonical, count):
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Home","item":"{SITE_URL}/"}},
        {{"@type":"ListItem","position":2,"name":"{esc_js(cat['label'])}","item":"{esc_js(canonical)}"}}
      ]
    }},
    {{
      "@type": "CollectionPage",
      "name": "{esc_js(cat['label'])} — {esc_js(SITE_NAME)}",
      "url": "{esc_js(canonical)}",
      "description": "{esc_js(cat.get('description',''))}",
      "numberOfItems": {count}
    }}
  ]
}}
</script>"""

# ══════════════════════════════════════════════
# NEW CATEGORIES AND WORKS DEFINITION (ENGLISH)
# ══════════════════════════════════════════════
CATEGORIES = [
  {"slug":"3d-print-models",    "label":"3D Print Models",     "icon":"🖨️", "description":"High-detail STL and OBJ 3D printable models, figurines, functional gadgets, and cosplay props."},
  {"slug":"powerpoint-templates","label":"PowerPoint Templates", "icon":"📊", "description":"Modern pitch deck templates, corporate business slides, and animated presentation designs."},
  {"slug":"indesign-templates",  "label":"InDesign Templates",   "icon":"📄", "description":"Editorial layouts, brochures, portfolio lookbooks, magazine spreads, and brand guidelines."},
  {"slug":"mockup-templates",    "label":"Mockup Templates",     "icon":"💻", "description":"Photorealistic PSD device scenes, packaging mockups, stationery branding, and apparel renders."},
  {"slug":"ui-design-kits",      "label":"UI Design Kits",       "icon":"🎨", "description":"Modern Figma UI kits, mobile app design systems, dashboard interfaces, and web components."}
]

WORKS = [
  # 3D Print Models
  {"slug":"cyberpunk-helmet-mk4",
   "title":"Cyberpunk Helmet MK-IV",
   "description":"High-fidelity wearable cosplay helmet designed for resin and FDM 3D printing. Features segmented modular plates, visor groove channels, and ventilation slots. Pre-supported STL files included with assembly guide.",
   "category":"3d-print-models","categoryLabel":"3D Print Models","date":"2026-09-24",
   "image":"/assets/images/placeholder-3d-1.svg","thumb":"/assets/images/placeholder-3d-1.svg",
   "emoji":"🪖","tags":["3D Printing","Cosplay","Cyberpunk","Wearable","STL"],"views":0,"source":"manual"},

  {"slug":"articulated-mech-dragon",
   "title":"Articulated Mech Dragon",
   "description":"Print-in-place flexible robotic dragon model requiring no supports or post-print assembly. Engineered with reinforced ball-and-socket hinge joints for fluid organic motion. Optimized for PLA and PETG filaments.",
   "category":"3d-print-models","categoryLabel":"3D Print Models","date":"2026-09-21",
   "image":"/assets/images/placeholder-3d-2.svg","thumb":"/assets/images/placeholder-3d-2.svg",
   "emoji":"🐉","tags":["Print in Place","Dragon","Mechanical","Toy","STL"],"views":0,"source":"manual"},

  {"slug":"hex-modular-desk-organizer",
   "title":"Hex Modular Desk Organizer",
   "description":"Interlocking hexagonal storage modules designed for creative workstations and electronics enthusiasts. Features magnetic side snaps, cable management routing, and customizable pen trays. Minimalist functional 3D print.",
   "category":"3d-print-models","categoryLabel":"3D Print Models","date":"2026-09-17",
   "image":"/assets/images/placeholder-3d-3.svg","thumb":"/assets/images/placeholder-3d-3.svg",
   "emoji":"⬡","tags":["Desk Organizer","Functional Print","Modular","Workspace"],"views":0,"source":"manual"},

  {"slug":"tabletop-scifi-titan-miniature",
   "title":"Sci-Fi Titan Warfare Miniature",
   "description":"28mm scale heroic warlord mecha sculpted for resin SLA/DLP 3D printers. Includes multiple interchangeable weapon loadouts, micro-detailed armor hydraulics, and scenic battleground base.",
   "category":"3d-print-models","categoryLabel":"3D Print Models","date":"2026-09-12",
   "image":"/assets/images/placeholder-3d-4.svg","thumb":"/assets/images/placeholder-3d-4.svg",
   "emoji":"🤖","tags":["Tabletop","Miniatures","Warhammer","Wargaming","Resin"],"views":0,"source":"manual"},

  # PowerPoint Templates
  {"slug":"pitch-deck-pro-presentation",
   "title":"Pitch Deck Pro Presentation",
   "description":"Venture capital ready investor pitch deck with 80+ unique slide layouts. Includes custom vector infographic charts, financial projection tables, and team profile cards. 16:9 widescreen format with master slide setup.",
   "category":"powerpoint-templates","categoryLabel":"PowerPoint Templates","date":"2026-09-22",
   "image":"/assets/images/placeholder-ppt-1.svg","thumb":"/assets/images/placeholder-ppt-1.svg",
   "emoji":"📈","tags":["Pitch Deck","Investor","Startup","Business","PPTX"],"views":0,"source":"manual"},

  {"slug":"minimal-annual-report-slides",
   "title":"Minimalist Business Report Slides",
   "description":"Clean Scandinavian style corporate review template designed for executive reporting and quarterly reviews. Features typographic hierarchy, editable data-driven charts, and drag-and-drop image placeholders.",
   "category":"powerpoint-templates","categoryLabel":"PowerPoint Templates","date":"2026-09-15",
   "image":"/assets/images/placeholder-ppt-2.svg","thumb":"/assets/images/placeholder-ppt-2.svg",
   "emoji":"📊","tags":["Annual Report","Corporate","Clean","Minimal","Presentation"],"views":0,"source":"manual"},

  {"slug":"creative-agency-portfolio-deck",
   "title":"Creative Agency Showreel Deck",
   "description":"Bold dark-mode presentation template designed for design studios and digital agencies. Includes video mockups, interactive transition cues, and case study showcase grids. Fully customizable color palette.",
   "category":"powerpoint-templates","categoryLabel":"PowerPoint Templates","date":"2026-09-08",
   "image":"/assets/images/placeholder-ppt-3.svg","thumb":"/assets/images/placeholder-ppt-3.svg",
   "emoji":"✨","tags":["Agency","Portfolio","Dark Mode","Showcase","Creative"],"views":0,"source":"manual"},

  # InDesign Templates
  {"slug":"modern-architecture-magazine",
   "title":"Modern Architecture Magazine Layout",
   "description":"Editorial 36-page magazine template formatted in A4 and US Letter sizes. Features 12-column grid alignment, master pages with automated page numbering, and paragraph styling. Ready for commercial offset printing.",
   "category":"indesign-templates","categoryLabel":"InDesign Templates","date":"2026-09-23",
   "image":"/assets/images/placeholder-id-1.svg","thumb":"/assets/images/placeholder-id-1.svg",
   "emoji":"🏛️","tags":["InDesign","Magazine","Editorial","Architecture","Print Ready"],"views":0,"source":"manual"},

  {"slug":"corporate-brand-guidelines-book",
   "title":"Corporate Brand Guidelines Booklet",
   "description":"Comprehensive 48-page identity manual covering logo usage, color systems, typography rules, and iconography specs. Built with Adobe InDesign character styles, swatches, and vector vector guides.",
   "category":"indesign-templates","categoryLabel":"InDesign Templates","date":"2026-09-16",
   "image":"/assets/images/placeholder-id-2.svg","thumb":"/assets/images/placeholder-id-2.svg",
   "emoji":"📘","tags":["Brand Book","Branding","Identity","Style Guide","INDD"],"views":0,"source":"manual"},

  {"slug":"minimal-photography-lookbook",
   "title":"Minimal Photography Lookbook",
   "description":"Elegant landscape photo book template focused on white space, fine-art captions, and full-bleed image spreads. Designed for fashion photographers, product designers, and artist portfolios.",
   "category":"indesign-templates","categoryLabel":"InDesign Templates","date":"2026-09-09",
   "image":"/assets/images/placeholder-id-3.svg","thumb":"/assets/images/placeholder-id-3.svg",
   "emoji":"📷","tags":["Lookbook","Photography","Portfolio","Landscape","InDesign"],"views":0,"source":"manual"},

  # Mockup Templates
  {"slug":"iphone-16-pro-floating-mockup",
   "title":"iPhone 16 Pro Titanium Mockup Kit",
   "description":"Hyper-realistic PSD device mockup featuring smart object layers for one-click screen replacement. Includes isolated shadows, customizable studio reflections, and titanium color variants. 6000×4000 px resolution.",
   "category":"mockup-templates","categoryLabel":"Mockup Templates","date":"2026-09-25",
   "image":"/assets/images/placeholder-mock-1.svg","thumb":"/assets/images/placeholder-mock-1.svg",
   "emoji":"📱","tags":["iPhone Mockup","Apple","PSD","Smart Object","Branding"],"views":0,"source":"manual"},

  {"slug":"hardcover-book-foil-stamp-mockup",
   "title":"Hardcover Book & Foil Stamp Mockup",
   "description":"Realistic book mockup with natural fabric linen texture and embossed metallic gold foil stamping effects. Fully separated background and shadow layers for custom presentation scenes.",
   "category":"mockup-templates","categoryLabel":"Mockup Templates","date":"2026-09-18",
   "image":"/assets/images/placeholder-mock-2.svg","thumb":"/assets/images/placeholder-mock-2.svg",
   "emoji":"📖","tags":["Book Mockup","Hardcover","Foil Stamp","Packaging","PSD"],"views":0,"source":"manual"},

  {"slug":"cosmetics-dropper-bottle-scene",
   "title":"Cosmetic Glass Dropper Bottle Scene",
   "description":"Minimalist luxury skincare bottle mockup with transparent glass refraction, metallic dropper cap, and textured paper label. Includes smart objects for instant label and liquid color updates.",
   "category":"mockup-templates","categoryLabel":"Mockup Templates","date":"2026-09-11",
   "image":"/assets/images/placeholder-mock-3.svg","thumb":"/assets/images/placeholder-mock-3.svg",
   "emoji":"🧴","tags":["Cosmetics","Packaging","Glass Bottle","Mockup","Realistic"],"views":0,"source":"manual"},

  # UI Design Kits
  {"slug":"fintech-crypto-dashboard-kit",
   "title":"Fintech & Crypto Dashboard Design System",
   "description":"Comprehensive Figma web dashboard design system with 120+ pre-built components and auto-layout 5.0 support. Includes dark and light UI variants, currency charts, transaction tables, and wallet balances.",
   "category":"ui-design-kits","categoryLabel":"UI Design Kits","date":"2026-09-26",
   "image":"/assets/images/placeholder-ui-1.svg","thumb":"/assets/images/placeholder-ui-1.svg",
   "emoji":"💳","tags":["Figma","UI Kit","Dashboard","Crypto","Design System"],"views":0,"source":"manual"},

  {"slug":"health-fitness-mobile-app-ui",
   "title":"Fitness & Workout Tracker iOS UI Kit",
   "description":"Modern iOS mobile application kit featuring 60+ responsive artboards in Figma. Covers onboarding flows, daily activity rings, workout timers, nutrition logs, and user profile management.",
   "category":"ui-design-kits","categoryLabel":"UI Design Kits","date":"2026-09-19",
   "image":"/assets/images/placeholder-ui-2.svg","thumb":"/assets/images/placeholder-ui-2.svg",
   "emoji":"🏃","tags":["Mobile App","iOS","Fitness","UI Kit","Figma"],"views":0,"source":"manual"},

  {"slug":"saas-analytics-web-components",
   "title":"SaaS Analytics Platform UI Kit",
   "description":"Scalable B2B web application kit with modular chart widgets, customizable data filters, role-based user management views, and interactive modals. Built with Figma design tokens and variants.",
   "category":"ui-design-kits","categoryLabel":"UI Design Kits","date":"2026-09-13",
   "image":"/assets/images/placeholder-ui-3.svg","thumb":"/assets/images/placeholder-ui-3.svg",
   "emoji":"📊","tags":["SaaS","Web App","Analytics","Components","Figma"],"views":0,"source":"manual"},

  {"slug":"ecommerce-store-design-system",
   "title":"Luxury eCommerce Storefront UI System",
   "description":"High-converting shopping experience kit covering modern product detail pages, sticky cart slide-outs, checkout multi-step wizard, and customer review modules. Ready for development handoff.",
   "category":"ui-design-kits","categoryLabel":"UI Design Kits","date":"2026-09-06",
   "image":"/assets/images/placeholder-ui-4.svg","thumb":"/assets/images/placeholder-ui-4.svg",
   "emoji":"🛍️","tags":["eCommerce","Shop","Storefront","UI Kit","Web Design"],"views":0,"source":"manual"}
]

# Write data files
os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "categories.json"), "w", encoding="utf-8") as f:
    json.dump(CATEGORIES, f, ensure_ascii=False, indent=2)
with open(os.path.join(DATA, "works.json"), "w", encoding="utf-8") as f:
    json.dump(WORKS, f, ensure_ascii=False, indent=2)

categories = CATEGORIES
works      = WORKS
cat_map    = {c["slug"]: c for c in categories}
works_by_cat = {}
for w in works:
    works_by_cat.setdefault(w["category"], []).append(w)

sorted_works = sorted(works, key=lambda w: w.get("date",""), reverse=True)
PER_PAGE = 12

# ── Navigation helpers ──────────────────────────
def nav_items(active_cat=None):
    items = [f'<li{"" if active_cat else " class=\"active\""}><a href="/">Home</a></li>']
    for c in categories:
        act = ' class="active"' if c["slug"] == active_cat else ""
        items.append(f'<li{act}><a href="/category/{c["slug"]}/">{esc(c["label"])}</a></li>')
    return "\n\t\t\t\t".join(items)

def side_nav(active_cat=None):
    items = ['<li><a href="/">🏠 Home</a></li>']
    for c in categories:
        act = " active" if c["slug"] == active_cat else ""
        items.append(f'<li class="{act.strip()}"><a href="/category/{c["slug"]}/">{esc(c["icon"])} {esc(c["label"])} <small style="color:#888;font-size:11px">({len(works_by_cat.get(c["slug"],[]))})</small></a></li>')
    return "\n\t\t\t\t\t\t".join(items)

# ── Header & Logo ──────────────────────────────
def logo_html():
    return """<a href="/" class="logo" aria-label="DIMSONSGFX Home">
\t\t\t\t<img src="/assets/images/logo-icon.png" alt="DIMSONSGFX" class="logo-icon" width="42" height="42">
\t\t\t\t<span class="logo-text">DIMSONS<span class="accent">GFX</span></span>
\t\t\t</a>"""

def header_html(active_cat=None):
    return f"""
\t<div class="wrap-main wrap-center">
\t\t<header class="header fx-row fx-middle">
\t\t\t{logo_html()}
\t\t\t<ul class="header-menu fx-row fx-start fx-1 to-mob">
\t\t\t\t{nav_items(active_cat)}
\t\t\t</ul>
\t\t\t<div class="search-btn js-search anim" aria-label="Search" title="Search"><span class="far fa-search"></span></div>
\t\t\t<button class="theme-toggle-btn" id="themeToggle" aria-label="Toggle theme" title="Toggle theme">☀️</button>
\t\t\t<div class="btn-menu" aria-label="Menu"><span class="far fa-bars"></span></div>
\t\t</header>
\t\t<!-- END HEADER -->"""

# ── Sidebar (ONLY CATEGORIES AS REQUESTED) ─────
def sidebar_left_html(active_cat=None):
    return f"""
\t\t\t<aside class="col-left fx-first" aria-label="Sidebar">
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Categories</div>
\t\t\t\t\t<ul class="header-menu side-menu">
\t\t\t\t\t\t{side_nav(active_cat)}
\t\t\t\t\t</ul>
\t\t\t\t</div>
\t\t\t</aside>
\t\t\t<!-- END COL-LEFT -->"""

def footer_html():
    return f"""
\t\t<footer class="footer fx-row fx-middle">
\t\t\t<div class="footer-copyright fx-1">&copy; {datetime.now().year} {esc(SITE_NAME)}. All rights reserved.</div>
\t\t</footer>
\t\t<!-- END FOOTER -->
\t\t</div><!-- END WRAP-MAIN -->
\t</div><!-- END WRAP -->"""

def search_overlay():
    return """
\t<div class="search-wrap" id="searchWrap" role="search">
\t\t<div class="search-header fx-row fx-middle">
\t\t\t<div class="search-title title">Search</div>
\t\t\t<div class="search-close" aria-label="Close search"><span class="far fa-times"></span></div>
\t\t</div>
\t\t<form id="quicksearch" method="get" action="/search/">
\t\t\t<div class="search-box">
\t\t\t\t<input id="story" name="q" placeholder="Search templates, models, mockups..." type="search" autocomplete="off" aria-label="Search query">
\t\t\t\t<button type="submit" aria-label="Submit search"><span class="far fa-search"></span></button>
\t\t\t</div>
\t\t</form>
\t</div>"""

def mobile_panel(active_cat=None):
    return f"""
\t<div class="close-overlay" aria-hidden="true"></div>
\t<div class="btn-close" aria-label="Close menu"><span class="far fa-times"></span></div>
\t<div class="side-panel" role="navigation" aria-label="Mobile Navigation">
\t\t<div style="font-weight:700;font-size:16px;margin-bottom:15px;color:#36c537">Menu</div>
\t\t<ul class="header-menu side-menu">
\t\t\t{nav_items(active_cat)}
\t\t</ul>
\t</div>"""

def scripts():
    return """
\t<button id="gotop" aria-label="Back to top" title="Back to top"><span class="far fa-arrow-up"></span></button>
\t<script src="/assets/js/libs.js"></script>
\t<script src="/assets/js/site.js"></script>"""

# ── Short item card (3 col, NO VIEWS ICON) ─────
def short_item(w):
    alt = img_alt(w)
    img_html = ""
    if w.get("thumb"):
        img_html = f'<img src="{esc(w["thumb"])}" alt="{esc(alt)}" loading="lazy" width="400" height="280">'
    else:
        img_html = f'<div class="no-image-placeholder" aria-label="{esc(alt)}">{w.get("emoji","🎨")}</div>'

    cat = cat_map.get(w.get("category",""), {})
    cat_label = cat.get("label", w.get("category",""))
    date_str  = fmt_date(w.get("date",""))
    desc = (w.get("description","") or "")[:140]
    if len(w.get("description","") or "") > 140:
        desc += "…"

    return f"""
<article class="short-item" itemscope itemtype="https://schema.org/CreativeWork">
\t<a class="short-link" href="/works/{esc(w['slug'])}/" title="{esc(alt)}">
\t\t<div class="short-img img-resp img-fit">
\t\t\t{img_html}
\t\t\t<div class="short-category">{esc(cat_label)}</div>
\t\t</div>
\t\t<div class="short-title title anim" itemprop="name">{esc(w['title'])}</div>
\t</a>
\t<div class="short-meta fx-row fx-middle icon-left">
\t\t<div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt" aria-hidden="true"></span><time datetime="{esc(w.get('date',''))}" itemprop="datePublished">{date_str}</time></div>
\t</div>
\t<div class="short-text" itemprop="description">{esc(desc)}</div>
\t<div class="short-bottom fx-row fx-middle">
\t\t<div class="fx-1"></div>
\t\t<a class="short-btn btn" href="/works/{esc(w['slug'])}/">View Details</a>
\t</div>
</article>"""

# ── Pagination ─────────────────────────────────
def pagination_html(current, total, base_url):
    if total <= 1: return ""
    pages = []
    if current > 1:
        prev_url = base_url if current-1 == 1 else f"{base_url}page/{current-1}/"
        pages.append(f'<li><a href="{prev_url}" aria-label="Previous page">← Prev</a></li>')
    for i in range(1, total+1):
        url = base_url if i == 1 else f"{base_url}page/{i}/"
        if i == current:
            pages.append(f'<li><span aria-current="page">{i}</span></li>')
        else:
            pages.append(f'<li><a href="{url}">{i}</a></li>')
    if current < total:
        next_url = f"{base_url}page/{current+1}/"
        pages.append(f'<li><a href="{next_url}" aria-label="Next page">Next →</a></li>')
    return f"""
<nav class="navigation" aria-label="Pagination">
\t<ul class="pagination">{''.join(pages)}</ul>
</nav>"""

# ══════════════════════════════════════════════
# GENERATE SVG PLACEHOLDERS
# ══════════════════════════════════════════════
IMG_DIR = os.path.join(BASE, "assets", "images")
os.makedirs(IMG_DIR, exist_ok=True)

SVG_CARD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0L0 0L0 40" fill="none" stroke="{ac}" stroke-width="0.3" opacity="0.15"/>
    </pattern>
  </defs>
  <rect width="800" height="560" fill="url(#bg)"/>
  <rect width="800" height="560" fill="url(#grid)"/>
  <circle cx="400" cy="255" r="130" fill="none" stroke="{ac}" stroke-width="1" opacity="0.2"/>
  <text x="400" y="235" font-size="60" text-anchor="middle" dominant-baseline="middle"
        font-family="Segoe UI Emoji,Apple Color Emoji,Noto Color Emoji,sans-serif">{emoji}</text>
  <text x="400" y="305" font-size="19" font-weight="600" text-anchor="middle"
        fill="{ac}" font-family="system-ui,sans-serif" opacity="0.9">{title}</text>
  <rect x="250" y="330" width="300" height="26" rx="13" fill="{ac}" opacity="0.1"/>
  <text x="400" y="347" font-size="12" text-anchor="middle"
        fill="{ac}" font-family="system-ui,sans-serif" opacity="0.8">{cat}</text>
</svg>"""

PLACEHOLDERS_DATA = [
    ("3d-1",   "#161a29","#0b0e17","#4fc3f7","🪖","Cyberpunk Helmet MK-IV",        "3D Print Models"),
    ("3d-2",   "#0e2417","#07130c","#66bb6a","🐉","Articulated Mech Dragon",       "3D Print Models"),
    ("3d-3",   "#1a1528","#0e0b16","#ab47bc","⬡","Hex Modular Desk Organizer",    "3D Print Models"),
    ("3d-4",   "#261414","#130909","#ef5350","🤖","Sci-Fi Titan Warfare Miniature", "3D Print Models"),

    ("ppt-1",  "#1f1807","#0f0c03","#ffa726","📈","Pitch Deck Pro Presentation",    "PowerPoint Templates"),
    ("ppt-2",  "#0a1c24","#040d12","#26c6da","📊","Minimalist Business Report",    "PowerPoint Templates"),
    ("ppt-3",  "#1c0e29","#0d0614","#ba68c8","✨","Creative Agency Showreel Deck",  "PowerPoint Templates"),

    ("id-1",   "#221019","#11070c","#ec407a","🏛️","Modern Architecture Magazine",  "InDesign Templates"),
    ("id-2",   "#0c1b26","#050c12","#29b6f6","📘","Corporate Brand Guidelines",     "InDesign Templates"),
    ("id-3",   "#171717","#0a0a0a","#bdbdbd","📷","Minimal Photography Lookbook",   "InDesign Templates"),

    ("mock-1", "#081c1c","#030c0c","#26a69a","📱","iPhone 16 Pro Mockup Kit",     "Mockup Templates"),
    ("mock-2", "#241808","#120b03","#ffb74d","📖","Hardcover Book Foil Stamp",     "Mockup Templates"),
    ("mock-3", "#1b1e10","#0d0f07","#9ccc65","🧴","Glass Dropper Bottle Scene",     "Mockup Templates"),

    ("ui-1",   "#0f1a30","#070c17","#5c6bc0","💳","Crypto Dashboard Design System", "UI Design Kits"),
    ("ui-2",   "#102419","#07120c","#4caf50","🏃","Fitness Tracker iOS UI Kit",     "UI Design Kits"),
    ("ui-3",   "#1a1426","#0c0912","#7e57c2","📊","SaaS Analytics Web Components", "UI Design Kits"),
    ("ui-4",   "#291515","#140909","#ff7043","🛍️","Luxury eCommerce Storefront UI", "UI Design Kits")
]

def darken(h, f=0.5):
    h = h.lstrip('#')
    r,g,b = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    return '#{:02x}{:02x}{:02x}'.format(int(r*f*255),int(g*f*255),int(b*f*255))

for slug, c1, c2, ac, emoji, title, cat in PLACEHOLDERS_DATA:
    svg = SVG_CARD.format(c1=c1, c2=darken(c1), ac=ac, emoji=emoji, title=title, cat=cat)
    with open(os.path.join(IMG_DIR, f"placeholder-{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# OG default image
og_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#1c2028"/>
  <defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0L0 0L0 40" fill="none" stroke="#36c537" stroke-width="0.4" opacity="0.08"/>
  </pattern></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="600" cy="315" r="210" fill="none" stroke="#36c537" stroke-width="1.5" opacity="0.15"/>
  <text x="600" y="275" font-size="56" font-weight="800" text-anchor="middle"
        fill="#f0f0f0" font-family="Montserrat,system-ui,sans-serif">DIMSONS<tspan fill="#36c537">GFX</tspan></text>
  <text x="600" y="340" font-size="21" text-anchor="middle"
        fill="#ccc" font-family="Rubik,system-ui,sans-serif">3D Print Models · Presentation Templates · UI Kits · Mockups</text>
  <text x="600" y="395" font-size="15" text-anchor="middle"
        fill="#666" font-family="system-ui,sans-serif">dimsonsgfx.github.io</text>
</svg>"""
with open(os.path.join(IMG_DIR, "og-default.svg"), "w", encoding="utf-8") as f:
    f.write(og_svg)

print(f"Generated {len(PLACEHOLDERS_DATA)} SVG cards + og-default.svg")

# ══════════════════════════════════════════════
# INDEX PAGE
# ══════════════════════════════════════════════
recent_cards = "\n".join(short_item(w) for w in sorted_works[:9])
all_cards    = "\n".join(short_item(w) for w in sorted_works)
og_img       = f"{SITE_URL}/assets/images/og-default.svg"
canonical    = f"{SITE_URL}/"

index_html = head_html(
    f"{SITE_NAME} — Digital Assets, 3D Models & Templates Portfolio",
    "Explore high-quality 3D print models, pitch deck templates, InDesign editorial layouts, mockup packages, and Figma UI design systems.",
    og_img, canonical,
    schema_website(),
    "website"
) + f"""
<body>
<div class="wrap">
{header_html()}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<div class="sect">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<h1 class="sect-title title fx-1">Latest Works</h1>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content" aria-label="Latest works">
{recent_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="sect" style="margin-top:20px">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<h2 class="sect-title title fx-1">All Works</h2>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content-all" aria-label="All works">
{all_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</main>
{sidebar_left_html()}
\t\t</div>
\t\t<!-- SEO description block -->
\t\t<div class="site-desc">
\t\t\t<h2>{esc(SITE_NAME)} — Creative Digital Assets & Templates</h2>
\t\t\t<p>Welcome to my official digital portfolio. Browse production-ready 3D print models, pitch deck presentations, professional InDesign publications, realistic packaging mockups, and scalable Figma UI design systems designed for creators and businesses.</p>
\t\t</div>
{footer_html()}
{search_overlay()}
{mobile_panel()}
{scripts()}
</div>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("Generated: index.html")

# ══════════════════════════════════════════════
# CATEGORY PAGES
# ══════════════════════════════════════════════
for cat in categories:
    slug  = cat["slug"]
    label = cat["label"]
    desc  = cat["description"]
    icon  = cat["icon"]
    cat_works = sorted(works_by_cat.get(slug,[]), key=lambda w: w.get("date",""), reverse=True)
    count     = len(cat_works)
    total_pages = max(1, (count + PER_PAGE - 1) // PER_PAGE)

    for page_num in range(1, total_pages + 1):
        page_works = cat_works[(page_num-1)*PER_PAGE : page_num*PER_PAGE]
        cards = "\n".join(short_item(w) for w in page_works)

        if page_num == 1:
            out_dir   = os.path.join(BASE, "category", slug)
            canonical = f"{SITE_URL}/category/{slug}/"
        else:
            out_dir   = os.path.join(BASE, "category", slug, "page", str(page_num))
            canonical = f"{SITE_URL}/category/{slug}/page/{page_num}/"
        os.makedirs(out_dir, exist_ok=True)

        og_img = og_image_url(page_works[0]) if page_works else f"{SITE_URL}/assets/images/og-default.svg"
        page_title = f"{label} — {SITE_NAME}" if page_num == 1 else f"{label} — Page {page_num} — {SITE_NAME}"
        meta_desc  = f"{desc} ({count} items in collection)."
        pagi       = pagination_html(page_num, total_pages, f"{SITE_URL}/category/{slug}/")

        html = head_html(page_title, meta_desc, og_img, canonical,
                         schema_category(cat, canonical, count)) + f"""
<body>
<div class="wrap">
{header_html(slug)}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<div class="sect">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<h1 class="sect-title title fx-1">{esc(icon)} {esc(label)}</h1>
\t\t\t\t\t</div>
\t\t\t\t\t<p style="color:#888;margin-bottom:20px;font-size:13px">{esc(desc)} · {count} items</p>
\t\t\t\t\t<div class="sect-content" id="dle-content">
{cards if cards else '<p style="color:#888;padding:20px 0">New items coming soon.</p>'}
\t\t\t\t\t</div>
\t\t\t\t</div>
{pagi}
\t\t\t</main>
{sidebar_left_html(slug)}
\t\t</div>
{footer_html()}
{search_overlay()}
{mobile_panel(slug)}
{scripts()}
</div>
</body>
</html>"""

        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Category: /category/{slug}/ ({count} works, {total_pages} pages)")

# ══════════════════════════════════════════════
# WORK DETAIL PAGES (NO VIEWS COUNTER)
# ══════════════════════════════════════════════
for w in works:
    slug      = w["slug"]
    cat_slug  = w["category"]
    cat       = cat_map.get(cat_slug, {"label": cat_slug, "icon":"🎨", "description":""})
    cat_label = cat["label"]
    cat_icon  = cat.get("icon","🎨")
    canonical = f"{SITE_URL}/works/{slug}/"
    og_img    = og_image_url(w)
    alt       = img_alt(w)
    date_str  = fmt_date(w.get("date",""))
    tags      = w.get("tags",[])
    desc      = w.get("description","") or alt
    meta_desc = desc[:155] + ("…" if len(desc) > 155 else "")

    img_html = ""
    if w.get("image"):
        img_html = f'<img src="{esc(w["image"])}" alt="{esc(alt)}" width="800" height="560" loading="eager" style="width:100%;height:auto;border-radius:4px;margin-bottom:30px;">'
    else:
        img_html = f'<div style="height:400px;background:var(--bg-secondary,#e8eaed);display:flex;align-items:center;justify-content:center;font-size:6rem;margin-bottom:30px;border-radius:4px;" aria-label="{esc(alt)}">{w.get("emoji","🎨")}</div>'

    tags_html = ""
    if tags:
        tags_html = '<div class="ftags"><span class="far fa-tags" aria-hidden="true"></span> '
        tags_html += " ".join(f'<a href="/search/?q={esc(t)}">{esc(t)}</a>' for t in tags)
        tags_html += "</div>"

    # Related works (same cat, max 3)
    related = [rw for rw in works if rw["category"] == cat_slug and rw["slug"] != slug][:3]
    related_html = ""
    if related:
        rcards = "\n".join(short_item(rw) for rw in related)
        related_html = f"""
\t\t\t\t<div class="sect side-box frels" style="margin-top:30px">
\t\t\t\t\t<div class="sect-header fx-row fx-middle">
\t\t\t\t\t\t<h2 class="sect-title fx-1 title" style="font-size:20px">Related Works:</h2>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content">{rcards}</div>
\t\t\t\t</div>"""

    html = head_html(
        f"{w['title']} — {SITE_NAME}",
        meta_desc, og_img, canonical,
        schema_work(w, canonical),
        "article"
    ) + f"""
<body>
<div class="wrap">
{header_html(cat_slug)}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<article class="article" itemscope itemtype="https://schema.org/CreativeWork">
\t\t\t\t<div class="fmain side-box">
\t\t\t\t\t<!-- Breadcrumb -->
\t\t\t\t\t<nav aria-label="Breadcrumb" style="font-size:13px;color:#888;margin-bottom:15px">
\t\t\t\t\t\t<a href="/">Home</a> › <a href="/category/{esc(cat_slug)}/">{esc(cat_label)}</a> › <span itemprop="name">{esc(w['title'])}</span>
\t\t\t\t\t</nav>
\t\t\t\t\t<h1 class="sect-title">{esc(w['title'])}</h1>
\t\t\t\t\t<div class="short-meta fx-row fx-middle icon-left" style="margin-bottom:25px">
\t\t\t\t\t\t<div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt" aria-hidden="true"></span><time datetime="{esc(w.get('date',''))}" itemprop="datePublished">{date_str}</time></div>
\t\t\t\t\t\t<div class="short-meta-item"><a href="/category/{esc(cat_slug)}/" itemprop="genre">{cat_icon} {esc(cat_label)}</a></div>
\t\t\t\t\t</div>
\t\t\t\t\t{img_html}
\t\t\t\t\t<div class="ftext full-text clearfix" itemprop="description">
\t\t\t\t\t\t<p>{esc(desc)}</p>
\t\t\t\t\t</div>
\t\t\t\t\t{tags_html}
\t\t\t\t\t<div class="fbtm fx-row fx-middle fbtm-one" style="margin-top:20px">
\t\t\t\t\t\t<div class="fx-1"></div>
\t\t\t\t\t\t<a href="/category/{esc(cat_slug)}/" class="btn">← Back to {esc(cat_label)}</a>
\t\t\t\t\t</div>
\t\t\t\t</div>
{related_html}
\t\t\t\t</article>
\t\t\t</main>
{sidebar_left_html(cat_slug)}
\t\t</div>
{footer_html()}
{search_overlay()}
{mobile_panel(cat_slug)}
{scripts()}
</div>
</body>
</html>"""

    out_dir = os.path.join(BASE, "works", slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

print(f"Works: {len(works)} pages")

# ══════════════════════════════════════════════
# SEARCH PAGE
# ══════════════════════════════════════════════
canonical = f"{SITE_URL}/search/"
search_page = head_html(
    f"Search — {SITE_NAME}",
    f"Search through {SITE_NAME} creative templates, 3D print models, and UI design kits.",
    f"{SITE_URL}/assets/images/og-default.svg",
    canonical
) + f"""
<body>
<div class="wrap">
{header_html()}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<div class="side-box">
\t\t\t\t\t<h1 class="mtitle">Search Portfolio</h1>
\t\t\t\t\t<form id="searchForm" role="search" style="margin-bottom:30px">
\t\t\t\t\t\t<div class="search-box" style="position:relative">
\t\t\t\t\t\t\t<input type="search" id="searchInput" name="q" placeholder="Type keywords..."
\t\t\t\t\t\t\t\taria-label="Search keywords"
\t\t\t\t\t\t\t\tstyle="width:100%;height:44px;padding:0 50px 0 15px;border:1px solid #e3e3e3;border-radius:4px;font-size:15px">
\t\t\t\t\t\t\t<button type="submit" aria-label="Submit search"
\t\t\t\t\t\t\t\tstyle="position:absolute;right:5px;top:2px;background:transparent;border:none;font-size:18px;cursor:pointer;color:#36c537;height:40px;width:40px">
\t\t\t\t\t\t\t\t<span class="far fa-search" aria-hidden="true"></span></button>
\t\t\t\t\t\t</div>
\t\t\t\t\t</form>
\t\t\t\t\t<div id="searchResults" style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:15px"></div>
\t\t\t\t</div>
\t\t\t</main>
{sidebar_left_html()}
\t\t</div>
{footer_html()}
{search_overlay()}
{mobile_panel()}
{scripts()}
<script>
document.addEventListener('DOMContentLoaded', async function() {{
  var params = new URLSearchParams(window.location.search);
  var q = params.get('q') || '';
  var inp = document.getElementById('searchInput');
  var res = document.getElementById('searchResults');
  if (inp) inp.value = q;
  if (!q) return;
  document.title = '"' + q + '" — Search — {esc(SITE_NAME)}';
  try {{
    var r = await fetch('/data/works.json');
    var works = await r.json();
    var ql = q.toLowerCase();
    var found = works.filter(function(w) {{
      return (w.title||'').toLowerCase().indexOf(ql) >= 0 ||
             (w.description||'').toLowerCase().indexOf(ql) >= 0 ||
             (w.tags||[]).some(function(t){{ return t.toLowerCase().indexOf(ql) >= 0; }}) ||
             (w.categoryLabel||'').toLowerCase().indexOf(ql) >= 0;
    }});
    if (!found.length) {{
      res.innerHTML = '<p style="color:#888;padding:20px 0">No results found for <strong>' + q.replace(/</g,'&lt;') + '</strong></p>';
    }} else {{
      res.innerHTML = found.map(function(w) {{ return renderShortItem(w); }}).join('');
      document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {{
        img.addEventListener('load', function(){{ img.classList.add('loaded'); }});
        if (img.complete) img.classList.add('loaded');
      }});
    }}
  }} catch(e) {{
    res.innerHTML = '<p style="color:#888">Error loading search database</p>';
  }}
  document.getElementById('searchForm').addEventListener('submit', function(e) {{
    e.preventDefault();
    var nq = inp.value.trim();
    if (nq) window.location.href = '/search/?q=' + encodeURIComponent(nq);
  }});
}});
</script>
</div>
</body>
</html>"""

os.makedirs(os.path.join(BASE, "search"), exist_ok=True)
with open(os.path.join(BASE, "search", "index.html"), "w", encoding="utf-8") as f:
    f.write(search_page)
print("Generated: /search/")

# ══════════════════════════════════════════════
# 404 PAGE
# ══════════════════════════════════════════════
page_404 = head_html(
    f"404 — Page Not Found · {SITE_NAME}",
    "The requested page could not be found.",
    f"{SITE_URL}/assets/images/og-default.svg",
    f"{SITE_URL}/404.html"
).replace('<meta name="robots" content="index, follow">',
          '<meta name="robots" content="noindex, follow">') + f"""
<body>
<div class="wrap">
{header_html()}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<div class="side-box" style="text-align:center;padding:60px 30px">
\t\t\t\t\t<div style="font-size:7rem;font-weight:800;color:#36c537;line-height:1">404</div>
\t\t\t\t\t<h1 style="font-size:22px;margin:20px 0 10px">Page Not Found</h1>
\t\t\t\t\t<p style="color:#888;margin-bottom:30px">The page you are looking for might have been removed or is temporarily unavailable.</p>
\t\t\t\t\t<a href="/" class="btn">← Back to Home</a>
\t\t\t\t</div>
\t\t\t</main>
{sidebar_left_html()}
\t\t</div>
{footer_html()}
{search_overlay()}
{mobile_panel()}
{scripts()}
</div>
</body>
</html>"""

with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
    f.write(page_404)
print("Generated: 404.html")

# ══════════════════════════════════════════════
# SITEMAP (with image:image)
# ══════════════════════════════════════════════
sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
]
sitemap_lines.append(f'  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>')
for cat in categories:
    sitemap_lines.append(
        f'  <url><loc>{SITE_URL}/category/{cat["slug"]}/</loc>'
        f'<changefreq>weekly</changefreq><priority>0.8</priority></url>'
    )
for w in sorted_works:
    img_url = og_image_url(w)
    alt     = img_alt(w)
    cap     = esc(w.get("title",""))
    lines = [
        f'  <url>',
        f'    <loc>{SITE_URL}/works/{w["slug"]}/</loc>',
        f'    <lastmod>{w.get("date", TODAY)}</lastmod>',
        f'    <changefreq>monthly</changefreq>',
        f'    <priority>0.6</priority>',
        f'    <image:image>',
        f'      <image:loc>{esc(img_url)}</image:loc>',
        f'      <image:title>{cap}</image:title>',
        f'      <image:caption>{esc(alt)}</image:caption>',
        f'    </image:image>',
        f'  </url>',
    ]
    sitemap_lines.extend(lines)
sitemap_lines.append('</urlset>')

with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_lines))
print("Generated: sitemap.xml")

# ══════════════════════════════════════════════
# ROBOTS.TXT
# ══════════════════════════════════════════════
robots = f"""User-agent: *
Allow: /
Disallow: /search/

Sitemap: {SITE_URL}/sitemap.xml
"""
with open(os.path.join(BASE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)
print("Generated: robots.txt")

# ── .nojekyll ────────────────────────────────
with open(os.path.join(BASE, ".nojekyll"), "w") as f:
    pass

total = 1 + len(categories) + len(works) + 2
print(f"\nBuild finished: {total} pages generated, {len(works)} works across {len(categories)} categories.")
