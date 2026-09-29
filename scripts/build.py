#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIMSONSGFX — Build script v2
Изменения:
  - Убрана правая колонка (col-right)
  - Посты в 3 столбца
  - Текстовый логотип-заглушка DIMSONSGFX
  - Полный SEO: JSON-LD ImageObject+BreadcrumbList, WebSite, Person
  - Image sitemap
  - Webmaster-теги (Google, Яндекс) — заглушки
  - Image alt из title + category
  - Canonical URL на каждой странице
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
# Оставляем пустыми — пользователь вставит свои коды в эти переменные
GOOGLE_VERIFICATION  = ""   # google-site-verification
YANDEX_VERIFICATION  = ""   # yandex-verification

# ── Load data ────────────────────────────────────
with open(os.path.join(DATA, "works.json"), encoding="utf-8-sig") as f:
    works = json.load(f)
with open(os.path.join(DATA, "categories.json"), encoding="utf-8-sig") as f:
    categories = json.load(f)

cat_map      = {c["slug"]: c for c in categories}
works_by_cat = {}
for w in works:
    works_by_cat.setdefault(w["category"], []).append(w)

# ── Helpers ──────────────────────────────────────
def esc(s):
    return str(s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def esc_js(s):
    return str(s or "").replace("\\","\\\\").replace('"','\\"').replace("\n"," ").replace("\r","")

def fmt_date(d):
    if not d: return ""
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        months = ["","января","февраля","марта","апреля","мая","июня",
                  "июля","августа","сентября","октября","ноября","декабря"]
        return f"{dt.day} {months[dt.month]} {dt.year}"
    except:
        return d

def pluralRu(n, f1="работа", f2="работы", f5="работ"):
    n = abs(int(n)) % 100
    n1 = n % 10
    if 10 < n < 20: return f5
    if 1 < n1 < 5:  return f2
    if n1 == 1:      return f1
    return f5

def img_alt(w):
    """Строим alt из title + category (никогда не пустой)."""
    cat = cat_map.get(w.get("category",""), {})
    cat_label = cat.get("label", w.get("category",""))
    return f"{w.get('title','')} — {cat_label}"

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
        tags.append('\t<!-- GOOGLE SEARCH CONSOLE: вставь свой код ниже (или в переменную GOOGLE_VERIFICATION в build.py) -->')
        tags.append('\t<!-- <meta name="google-site-verification" content="ТВОЙ_КОД"> -->')
    if YANDEX_VERIFICATION:
        tags.append(f'\t<meta name="yandex-verification" content="{esc(YANDEX_VERIFICATION)}">')
    else:
        tags.append('\t<!-- ЯНДЕКС ВЕБМАСТЕР: вставь свой код ниже -->')
        tags.append('\t<!-- <meta name="yandex-verification" content="ТВОЙ_КОД"> -->')
    return "\n".join(tags)

# ── Theme init (no flash) ─────────────────────
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

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&family=Rubik:wght@300;400;500&display=swap&subset=cyrillic" rel="stylesheet">'

# ── <head> ────────────────────────────────────
def head_html(title, desc, og_img, canonical, schema_ld="", page_type="website"):
    wm = webmaster_meta()
    return f"""<!DOCTYPE html>
<html lang="ru">
{THEME_INIT}
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">

\t<!-- SEO -->
\t<title>{esc(title)}</title>
\t<meta name="description" content="{esc(desc)}">
\t<link rel="canonical" href="{esc(canonical)}">
\t<meta name="robots" content="index, follow">

\t<!-- Open Graph -->
\t<meta property="og:title" content="{esc(title)}">
\t<meta property="og:description" content="{esc(desc)}">
\t<meta property="og:image" content="{esc(og_img)}">
\t<meta property="og:image:width" content="1200">
\t<meta property="og:image:height" content="630">
\t<meta property="og:url" content="{esc(canonical)}">
\t<meta property="og:type" content="{page_type}">
\t<meta property="og:locale" content="ru_RU">
\t<meta property="og:site_name" content="{esc(SITE_NAME)}">

\t<!-- Twitter Card -->
\t<meta name="twitter:card" content="summary_large_image">
\t<meta name="twitter:title" content="{esc(title)}">
\t<meta name="twitter:description" content="{esc(desc)}">
\t<meta name="twitter:image" content="{esc(og_img)}">

\t<!-- Webmaster -->
{wm}

\t<!-- Icons -->
\t<link rel="shortcut icon" href="/assets/images/favicon.png" type="image/png">
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
      "description": "Портфолио цифрового художника: арты, логотипы, баннеры, иллюстрации",
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
        {{"@type":"ListItem","position":1,"name":"Главная","item":"{SITE_URL}/"}},
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
        {{"@type":"ListItem","position":1,"name":"Главная","item":"{SITE_URL}/"}},
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

# ── Nav helpers ────────────────────────────────
def nav_items(active_cat=None):
    items = [f'<li{"" if active_cat else " class=\"active\""}><a href="/">Главная</a></li>']
    for c in categories:
        act = ' class="active"' if c["slug"] == active_cat else ""
        items.append(f'<li{act}><a href="/category/{c["slug"]}/">{esc(c["label"])}</a></li>')
    return "\n\t\t\t\t".join(items)

def side_nav(active_cat=None):
    items = ['<li><a href="/">Главная</a></li>']
    for c in categories:
        act = " active" if c["slug"] == active_cat else ""
        items.append(f'<li class="{act.strip()}"><a href="/category/{c["slug"]}/">{esc(c["icon"])} {esc(c["label"])}</a></li>')
    return "\n\t\t\t\t\t\t".join(items)

# ── Page parts ─────────────────────────────────
def logo_html():
    return '<a href="/" class="logo" aria-label="DIMSONSGFX — на главную"><span class="logo-text">DIMSONS<span class="accent">GFX</span></span></a>'

def header_html(active_cat=None):
    return f"""
\t<div class="wrap-main wrap-center">
\t\t<header class="header fx-row fx-middle">
\t\t\t{logo_html()}
\t\t\t<ul class="header-menu fx-row fx-start fx-1 to-mob">
\t\t\t\t{nav_items(active_cat)}
\t\t\t</ul>
\t\t\t<div class="search-btn js-search anim" aria-label="Поиск"><span class="far fa-search"></span></div>
\t\t\t<button class="theme-toggle-btn" id="themeToggle" aria-label="Переключить тему" title="Сменить тему">☀️</button>
\t\t\t<div class="btn-menu"><span class="far fa-bars"></span></div>
\t\t</header>
\t\t<!-- END HEADER -->"""

def sidebar_left_html(active_cat=None):
    return f"""
\t\t\t<aside class="col-left fx-first" aria-label="Боковая панель">
\t\t\t\t<div class="side-box to-mob">
\t\t\t\t\t<div class="side-bt title">Навигация</div>
\t\t\t\t\t<ul class="header-menu side-menu">
\t\t\t\t\t\t{side_nav(active_cat)}
\t\t\t\t\t</ul>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Выбор редакции</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" id="sidebar-editor-pick">
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Топ работ</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" data-sidebar="top" data-limit="8">
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</aside>
\t\t\t<!-- END COL-LEFT -->"""

def footer_html():
    return f"""
\t\t<footer class="footer fx-row fx-middle">
\t\t\t<div class="footer-copyright fx-1">© {datetime.now().year} {esc(SITE_NAME)}. Все права защищены.</div>
\t\t</footer>
\t\t<!-- END FOOTER -->
\t\t</div><!-- END WRAP-MAIN -->
\t</div><!-- END WRAP -->"""

def search_overlay():
    return """
\t<div class="search-wrap" id="searchWrap" role="search">
\t\t<div class="search-header fx-row fx-middle">
\t\t\t<div class="search-title title">Поиск</div>
\t\t\t<div class="search-close" aria-label="Закрыть"><span class="far fa-times"></span></div>
\t\t</div>
\t\t<form id="quicksearch" method="get" action="/search/">
\t\t\t<div class="search-box">
\t\t\t\t<input id="story" name="q" placeholder="Поиск по сайту..." type="search" autocomplete="off" aria-label="Поисковый запрос">
\t\t\t\t<button type="submit" aria-label="Найти"><span class="far fa-search"></span></button>
\t\t\t</div>
\t\t</form>
\t</div>"""

def mobile_panel(active_cat=None):
    return f"""
\t<div class="close-overlay" aria-hidden="true"></div>
\t<div class="btn-close" aria-label="Закрыть меню"><span class="far fa-times"></span></div>
\t<div class="side-panel" role="navigation" aria-label="Мобильное меню">
\t\t<ul class="header-menu side-menu">
\t\t\t{nav_items(active_cat)}
\t\t</ul>
\t</div>"""

def scripts():
    return """
\t<button id="gotop" aria-label="Наверх"><span class="far fa-arrow-up"></span></button>
\t<script src="/assets/js/libs.js"></script>
\t<script src="/assets/js/site.js"></script>"""

# ── Short item card (3 col) ────────────────────
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
\t\t<div class="short-meta-item"><span class="far fa-eye" aria-hidden="true"></span>{w.get('views',0)}</div>
\t</div>
\t<div class="short-text" itemprop="description">{esc(desc)}</div>
\t<div class="short-bottom fx-row fx-middle">
\t\t<div class="fx-1"></div>
\t\t<a class="short-btn btn" href="/works/{esc(w['slug'])}/">Подробнее</a>
\t</div>
</article>"""

# ── Pagination ─────────────────────────────────
def pagination_html(current, total, base_url):
    if total <= 1: return ""
    pages = []
    if current > 1:
        prev_url = base_url if current-1 == 1 else f"{base_url}page/{current-1}/"
        pages.append(f'<li><a href="{prev_url}" aria-label="Предыдущая">← Пред.</a></li>')
    for i in range(1, total+1):
        url = base_url if i == 1 else f"{base_url}page/{i}/"
        if i == current:
            pages.append(f'<li><span aria-current="page">{i}</span></li>')
        else:
            pages.append(f'<li><a href="{url}">{i}</a></li>')
    if current < total:
        next_url = f"{base_url}page/{current+1}/"
        pages.append(f'<li><a href="{next_url}" aria-label="Следующая">След. →</a></li>')
    return f"""
<nav class="navigation" aria-label="Страницы">
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
  <rect x="300" y="330" width="200" height="26" rx="13" fill="{ac}" opacity="0.1"/>
  <text x="400" y="347" font-size="11" text-anchor="middle"
        fill="{ac}" font-family="system-ui,sans-serif" opacity="0.75">{cat}</text>
</svg>"""

PLACEHOLDERS = [
    ("arts-1",         "#1a1a2e","#0c0c1a","#c8a96e","🌆","Urban Dreams",         "Арты"),
    ("arts-2",         "#0d2818","#071510","#4ecca3","🌿","Neon Forest",           "Арты"),
    ("arts-3",         "#0a0a1a","#050510","#7c6fcd","🚀","Cosmic Voyage",         "Арты"),
    ("arts-4",         "#001525","#000d18","#0088cc","🌊","Deep Sea",              "Арты"),
    ("logos-1",        "#1a1a1a","#0e0e0e","#c8a96e","◎","Minimalist Mark",       "Логотипы"),
    ("logos-2",        "#1a0a0a","#0e0505","#cc4444","🐻","The Beast Co.",         "Логотипы"),
    ("logos-3",        "#1a0f08","#0e0904","#c87941","☕","Brew & Soul",           "Логотипы"),
    ("logos-4",        "#0a1020","#060a15","#4488ff","⬡","Nexus Labs",            "Логотипы"),
    ("banners-1",      "#1a1500","#0e0e00","#ffcc00","☀️","Summer Sale 2026",     "Баннеры"),
    ("banners-2",      "#050510","#030308","#8855ff","🎤","Night Conference",      "Баннеры"),
    ("banners-3",      "#001a10","#00100a","#00cc77","📱","App Launch",            "Баннеры"),
    ("illustrations-1","#1a2a10","#101a08","#88cc44","🦊","Лесные истории",       "Иллюстрации"),
    ("illustrations-2","#0a1020","#060a15","#4499ff","🧠","Digital Minds",        "Иллюстрации"),
    ("illustrations-3","#1a0a20","#0e0515","#cc44aa","🎭","Faceless",             "Иллюстрации"),
    ("other-1",        "#201505","#140e03","#cc9944","🗺️","Treasure Map",        "Прочее"),
    ("other-2",        "#0a1a20","#060f15","#44aacc","🔷","Aztec Pattern",        "Прочее"),
    ("other-3",        "#050a10","#03060a","#3388ff","📊","Analytics Dashboard",  "Прочее"),
]

def darken(h, f=0.5):
    h = h.lstrip('#')
    r,g,b = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    return '#{:02x}{:02x}{:02x}'.format(int(r*f*255),int(g*f*255),int(b*f*255))

for slug, c1, c2, ac, emoji, title, cat in PLACEHOLDERS:
    svg = SVG_CARD.format(c1=c1, c2=darken(c1), ac=ac, emoji=emoji, title=title, cat=cat)
    with open(os.path.join(IMG_DIR, f"placeholder-{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# OG default image
og_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#22272e"/>
  <defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0L0 0L0 40" fill="none" stroke="#36c537" stroke-width="0.4" opacity="0.08"/>
  </pattern></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="600" cy="315" r="200" fill="none" stroke="#36c537" stroke-width="1" opacity="0.1"/>
  <text x="600" y="278" font-size="54" font-weight="800" text-anchor="middle"
        fill="#f0f0f0" font-family="system-ui,sans-serif">DIMSONSGFX</text>
  <text x="600" y="345" font-size="22" text-anchor="middle"
        fill="#36c537" font-family="system-ui,sans-serif">Арты · Логотипы · Баннеры · Иллюстрации</text>
  <text x="600" y="400" font-size="15" text-anchor="middle"
        fill="#666" font-family="system-ui,sans-serif">dimsonsgfx.github.io</text>
</svg>"""
with open(os.path.join(IMG_DIR, "og-default.svg"), "w", encoding="utf-8") as f:
    f.write(og_svg)

print(f"SVG placeholders: {len(PLACEHOLDERS)} + og-default")

# ══════════════════════════════════════════════
# DATA FILES
# ══════════════════════════════════════════════
WORKS = [
  {"slug":"urban-dreams","title":"Urban Dreams","description":"Городской пейзаж в стиле ретро-футуризм — неоновые огни и дождливые ночные улицы. Работа вдохновлена эстетикой ретро-города будущего. Создана в Adobe Photoshop.","category":"arts","categoryLabel":"Арты","date":"2026-09-20","image":"/assets/images/placeholder-arts-1.svg","thumb":"/assets/images/placeholder-arts-1.svg","emoji":"🌆","tags":["иллюстрация","город","ретро","ночь"],"views":142,"source":"manual"},
  {"slug":"neon-forest","title":"Neon Forest","description":"Фантастический лес с биолюминесцентными растениями и туманом. Каждый элемент светится изнутри — природа встречает фантастику. Цифровая живопись.","category":"arts","categoryLabel":"Арты","date":"2026-09-15","image":"/assets/images/placeholder-arts-2.svg","thumb":"/assets/images/placeholder-arts-2.svg","emoji":"🌿","tags":["природа","фэнтези","свет","биолюминесценция"],"views":98,"source":"manual"},
  {"slug":"cosmic-voyage","title":"Cosmic Voyage","description":"Путешествие сквозь галактику — абстрактная цифровая живопись со звёздными туманностями. Работа исследует тему бесконечности космоса. Выполнена в Procreate.","category":"arts","categoryLabel":"Арты","date":"2026-09-10","image":"/assets/images/placeholder-arts-3.svg","thumb":"/assets/images/placeholder-arts-3.svg","emoji":"🚀","tags":["космос","абстракция","галактика"],"views":201,"source":"manual"},
  {"slug":"deep-sea","title":"Deep Sea","description":"Загадочные глубины океана — светящиеся медузы и загадочные морские существа в темноте. Работа передаёт атмосферу недостижимых глубин. Цифровая иллюстрация.","category":"arts","categoryLabel":"Арты","date":"2026-09-05","image":"/assets/images/placeholder-arts-4.svg","thumb":"/assets/images/placeholder-arts-4.svg","emoji":"🌊","tags":["море","фэнтези","медузы","глубина"],"views":77,"source":"manual"},
  {"slug":"logo-minimalist","title":"Minimalist Mark","description":"Логотип для студии дизайна — чистые линии и принцип золотого сечения. Знак построен на сетке из 8 единиц, акцент на геометрическую точность. Выполнен в Illustrator.","category":"logos","categoryLabel":"Логотипы","date":"2026-09-18","image":"/assets/images/placeholder-logos-1.svg","thumb":"/assets/images/placeholder-logos-1.svg","emoji":"◎","tags":["минимализм","геометрия","брендинг","студия"],"views":315,"source":"manual"},
  {"slug":"logo-beast","title":"The Beast Co.","description":"Агрессивный логотип для спортивного бренда — медведь в геометрическом стиле low-poly. Форма зверя скрыта в треугольной сетке. Брендинг для фитнес-компании.","category":"logos","categoryLabel":"Логотипы","date":"2026-09-12","image":"/assets/images/placeholder-logos-2.svg","thumb":"/assets/images/placeholder-logos-2.svg","emoji":"🐻","tags":["спорт","животное","геометрия","low-poly"],"views":189,"source":"manual"},
  {"slug":"logo-coffee","title":"Brew & Soul","description":"Уютный логотип для кофейни с ручной типографикой и стилизованным паром. Тёплая атмосфера и домашний уют передаются через округлые формы. Hand-lettering.","category":"logos","categoryLabel":"Логотипы","date":"2026-09-08","image":"/assets/images/placeholder-logos-3.svg","thumb":"/assets/images/placeholder-logos-3.svg","emoji":"☕","tags":["кофе","типографика","hand-lettering","уют"],"views":94,"source":"manual"},
  {"slug":"logo-tech","title":"Nexus Labs","description":"Современный логотип для IT-стартапа — узлы сети, соединения и данные. Гексагональная форма символизирует масштабируемость и связанность. Минималистичный tech-стиль.","category":"logos","categoryLabel":"Логотипы","date":"2026-09-02","image":"/assets/images/placeholder-logos-4.svg","thumb":"/assets/images/placeholder-logos-4.svg","emoji":"⬡","tags":["технологии","IT","гексагон","минимализм"],"views":122,"source":"manual"},
  {"slug":"banner-sale","title":"Summer Sale 2026","description":"Анимированный баннер для интернет-магазина — летняя акция с яркими акцентами. Акцент на скорость и выгоду через динамичную типографику. Форматы 728×90, 300×250, 160×600.","category":"banners","categoryLabel":"Баннеры","date":"2026-09-22","image":"/assets/images/placeholder-banners-1.svg","thumb":"/assets/images/placeholder-banners-1.svg","emoji":"☀️","tags":["реклама","акция","лето","e-commerce"],"views":267,"source":"manual"},
  {"slug":"banner-event","title":"Night Conference","description":"Баннер для онлайн-конференции по технологиям — тёмная тема с частицами и неоновыми акцентами. Передаёт атмосферу ночного digital-события. Анимированный HTML5.","category":"banners","categoryLabel":"Баннеры","date":"2026-09-16","image":"/assets/images/placeholder-banners-2.svg","thumb":"/assets/images/placeholder-banners-2.svg","emoji":"🎤","tags":["конференция","тёмная тема","технологии","HTML5"],"views":88,"source":"manual"},
  {"slug":"banner-app","title":"App Launch","description":"Промо-баннер для запуска мобильного приложения — чистый дизайн с фокусом на CTA. Использованы реальные экраны приложения на устройстве. Для App Store и Google Play.","category":"banners","categoryLabel":"Баннеры","date":"2026-09-11","image":"/assets/images/placeholder-banners-3.svg","thumb":"/assets/images/placeholder-banners-3.svg","emoji":"📱","tags":["мобайл","запуск","App Store","промо"],"views":156,"source":"manual"},
  {"slug":"children-book","title":"Лесные истории","description":"Иллюстрации для детской книги — добрые персонажи и сказочный лес с грибами и ягодами. Стиль — мягкие акварельные текстуры. Серия из 12 иллюстраций.","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-19","image":"/assets/images/placeholder-illustrations-1.svg","thumb":"/assets/images/placeholder-illustrations-1.svg","emoji":"🦊","tags":["детская","книга","персонажи","акварель"],"views":203,"source":"manual"},
  {"slug":"editorial-tech","title":"Digital Minds","description":"Редакционная иллюстрация о влиянии технологий на человека — мозг и микросхемы. Создана для журнала о цифровой трансформации. Метафора цифрового разума.","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-14","image":"/assets/images/placeholder-illustrations-2.svg","thumb":"/assets/images/placeholder-illustrations-2.svg","emoji":"🧠","tags":["редакционная","технологии","метафора","журнал"],"views":67,"source":"manual"},
  {"slug":"portrait-abstract","title":"Faceless","description":"Абстрактный портрет — образ человека разложен на геометрические плоскости и формы. Исследование идентичности через деконструкцию лица. Серия из 5 работ.","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-09","image":"/assets/images/placeholder-illustrations-3.svg","thumb":"/assets/images/placeholder-illustrations-3.svg","emoji":"🎭","tags":["портрет","геометрия","абстракция","идентичность"],"views":144,"source":"manual"},
  {"slug":"map-treasure","title":"Treasure Map","description":"Стилизованная карта сокровищ в пиратской тематике — старинный пергамент с символами и маршрутом. Ручная текстура и состаренные эффекты. Для настольной игры.","category":"other","categoryLabel":"Прочее","date":"2026-09-17","image":"/assets/images/placeholder-other-1.svg","thumb":"/assets/images/placeholder-other-1.svg","emoji":"🗺️","tags":["карта","пираты","игра","состаривание"],"views":55,"source":"manual"},
  {"slug":"pattern-aztec","title":"Aztec Pattern","description":"Орнаментальный паттерн в ацтекском стиле для текстиля и принтов — симметричный геометрический рисунок. Вдохновлён древними рукописями. Бесшовный тайл 2000×2000 px.","category":"other","categoryLabel":"Прочее","date":"2026-09-13","image":"/assets/images/placeholder-other-2.svg","thumb":"/assets/images/placeholder-other-2.svg","emoji":"🔷","tags":["паттерн","орнамент","ацтеки","текстиль"],"views":81,"source":"manual"},
  {"slug":"ui-dashboard","title":"Analytics Dashboard","description":"UI-дизайн дашборда аналитики — тёмная тема, графики, карточки с KPI и боковое меню. Адаптивный дизайн для desktop и tablet. Выполнен в Figma.","category":"other","categoryLabel":"Прочее","date":"2026-09-07","image":"/assets/images/placeholder-other-3.svg","thumb":"/assets/images/placeholder-other-3.svg","emoji":"📊","tags":["UI","Figma","дашборд","тёмная тема"],"views":119,"source":"manual"},
]

CATEGORIES = [
  {"slug":"arts","label":"Арты","icon":"🎨","description":"Цифровые арты, концепт-арт и авторские иллюстрации в различных стилях"},
  {"slug":"logos","label":"Логотипы","icon":"✦","description":"Разработка логотипов и визуальной идентичности для брендов и компаний"},
  {"slug":"banners","label":"Баннеры","icon":"🖼","description":"Рекламные баннеры, промо-материалы и визуальный контент для digital"},
  {"slug":"illustrations","label":"Иллюстрации","icon":"✏️","description":"Редакционные иллюстрации, детские книги и авторские персонажи"},
  {"slug":"other","label":"Прочее","icon":"💎","description":"Паттерны, UI-дизайн, карты, текстуры и экспериментальные работы"},
]

with open(os.path.join(DATA, "works.json"), "w", encoding="utf-8") as f:
    json.dump(WORKS, f, ensure_ascii=False, indent=2)
with open(os.path.join(DATA, "categories.json"), "w", encoding="utf-8") as f:
    json.dump(CATEGORIES, f, ensure_ascii=False, indent=2)

# Reload
works      = WORKS
categories = CATEGORIES
cat_map    = {c["slug"]: c for c in categories}
works_by_cat = {}
for w in works:
    works_by_cat.setdefault(w["category"], []).append(w)

print("Data files written")
sorted_works = sorted(works, key=lambda w: w.get("date",""), reverse=True)
PER_PAGE = 12

# ══════════════════════════════════════════════
# INDEX PAGE
# ══════════════════════════════════════════════
recent_cards = "\n".join(short_item(w) for w in sorted_works[:9])
all_cards    = "\n".join(short_item(w) for w in sorted_works)
og_img       = f"{SITE_URL}/assets/images/og-default.svg"
canonical    = f"{SITE_URL}/"

index_html = head_html(
    f"{SITE_NAME} — Портфолио цифрового художника",
    "Портфолио цифрового художника DIMSONSGFX: арты, логотипы, баннеры, иллюстрации. Авторские работы в разных стилях.",
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
\t\t\t\t\t\t<h1 class="sect-title title fx-1">Последние работы</h1>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content" aria-label="Список работ">
{recent_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="sect" style="margin-top:10px">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<h2 class="sect-title title fx-1">Все работы</h2>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content-all" aria-label="Все работы">
{all_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</main>
{sidebar_left_html()}
\t\t</div>
\t\t<!-- SEO description -->
\t\t<div class="site-desc">
\t\t\t<h2>{esc(SITE_NAME)} — портфолио цифрового художника</h2>
\t\t\t<p>Добро пожаловать в портфолио! Здесь собраны авторские работы: цифровые арты, логотипы, баннеры и иллюстрации. Каждая работа создана с вниманием к деталям.</p>
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

        # OG image = first work's thumb
        og_img = og_image_url(page_works[0]) if page_works else f"{SITE_URL}/assets/images/og-default.svg"
        page_title = f"{label} — {SITE_NAME}" if page_num == 1 else f"{label} — стр. {page_num} — {SITE_NAME}"
        meta_desc  = f"{desc}. {count} {pluralRu(count)} в портфолио."
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
\t\t\t\t\t<p style="color:#888;margin-bottom:20px;font-size:13px">{esc(desc)} · {count} {pluralRu(count)}</p>
\t\t\t\t\t<div class="sect-content" id="dle-content">
{cards if cards else '<p style="color:#888;padding:20px 0">Работы появятся здесь совсем скоро</p>'}
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
# WORK DETAIL PAGES
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
    # Title: description first sentence as meta desc
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
\t\t\t\t\t\t<h2 class="sect-title fx-1 title" style="font-size:20px">Читайте также:</h2>
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
\t\t\t\t\t<nav aria-label="Хлебные крошки" style="font-size:13px;color:#888;margin-bottom:15px">
\t\t\t\t\t\t<a href="/">Главная</a> › <a href="/category/{esc(cat_slug)}/">{esc(cat_label)}</a> › <span itemprop="name">{esc(w['title'])}</span>
\t\t\t\t\t</nav>
\t\t\t\t\t<h1 class="sect-title">{esc(w['title'])}</h1>
\t\t\t\t\t<div class="short-meta fx-row fx-middle icon-left" style="margin-bottom:25px">
\t\t\t\t\t\t<div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt" aria-hidden="true"></span><time datetime="{esc(w.get('date',''))}" itemprop="datePublished">{date_str}</time></div>
\t\t\t\t\t\t<div class="short-meta-item"><span class="far fa-eye" aria-hidden="true"></span>{w.get('views',0)}</div>
\t\t\t\t\t\t<div class="short-meta-item"><a href="/category/{esc(cat_slug)}/" itemprop="genre">{cat_icon} {esc(cat_label)}</a></div>
\t\t\t\t\t</div>
\t\t\t\t\t{img_html}
\t\t\t\t\t<div class="ftext full-text clearfix" itemprop="description">
\t\t\t\t\t\t<p>{esc(desc)}</p>
\t\t\t\t\t</div>
\t\t\t\t\t{tags_html}
\t\t\t\t\t<div class="fbtm fx-row fx-middle fbtm-one" style="margin-top:20px">
\t\t\t\t\t\t<div class="fx-1"></div>
\t\t\t\t\t\t<a href="/category/{esc(cat_slug)}/" class="btn">← К категории {esc(cat_label)}</a>
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
    f"Поиск — {SITE_NAME}",
    f"Поиск по портфолио {SITE_NAME}. Найдите арты, логотипы, баннеры и иллюстрации.",
    f"{SITE_URL}/assets/images/og-default.svg",
    canonical
) + f"""
<body>
<div class="wrap">
{header_html()}
\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main" id="main-content">
\t\t\t\t<div class="side-box">
\t\t\t\t\t<h1 class="mtitle">Поиск</h1>
\t\t\t\t\t<form id="searchForm" role="search" style="margin-bottom:30px">
\t\t\t\t\t\t<div class="search-box" style="position:relative">
\t\t\t\t\t\t\t<input type="search" id="searchInput" name="q" placeholder="Введите запрос..."
\t\t\t\t\t\t\t\taria-label="Поисковый запрос"
\t\t\t\t\t\t\t\tstyle="width:100%;height:44px;padding:0 50px 0 15px;border:1px solid #e3e3e3;border-radius:4px;font-size:15px">
\t\t\t\t\t\t\t<button type="submit" aria-label="Найти"
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
  document.title = '"' + q + '" — Поиск — {esc(SITE_NAME)}';
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
      res.innerHTML = '<p style="color:#888;padding:20px 0">По запросу <strong>' + q.replace(/</g,'&lt;') + '</strong> ничего не найдено</p>';
    }} else {{
      res.innerHTML = found.map(function(w) {{ return renderShortItem(w); }}).join('');
      document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {{
        img.addEventListener('load', function(){{ img.classList.add('loaded'); }});
        if (img.complete) img.classList.add('loaded');
      }});
    }}
  }} catch(e) {{
    res.innerHTML = '<p style="color:#888">Ошибка загрузки данных</p>';
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
    f"404 — Страница не найдена · {SITE_NAME}",
    "Запрашиваемая страница не найдена.",
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
\t\t\t\t\t<h1 style="font-size:22px;margin:20px 0 10px">Страница не найдена</h1>
\t\t\t\t\t<p style="color:#888;margin-bottom:30px">Возможно, она была удалена или вы перешли по устаревшей ссылке.</p>
\t\t\t\t\t<a href="/" class="btn">← На главную</a>
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
# SITEMAP (с image:image)
# ══════════════════════════════════════════════
sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
]
# Index
sitemap_lines.append(f'  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>')
# Categories
for cat in categories:
    sitemap_lines.append(
        f'  <url><loc>{SITE_URL}/category/{cat["slug"]}/</loc>'
        f'<changefreq>weekly</changefreq><priority>0.8</priority></url>'
    )
# Works (with image entries)
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
print("Generated: sitemap.xml (with image sitemap)")

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

total = 1 + len(categories) + len(works) + 2  # index + cats + works + search + 404
print(f"\nBuild complete: {total} pages, {len(works)} works, {len(categories)} cats")
