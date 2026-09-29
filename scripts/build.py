#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIMSONSGFX — Build script
Генерирует все статические страницы из JSON-данных,
точно воспроизводя макет шаблона avaxgfxgreen DLE.
"""
import json, os, re
from datetime import datetime

SITE_URL = "https://dimsonsgfx.github.io"
BASE = r"C:\Users\dimso\dimsonsgfx-site"
DATA = os.path.join(BASE, "data")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── Load data ──────────────────────────────────
with open(os.path.join(DATA, "works.json"), encoding="utf-8-sig") as f:
    works = json.load(f)
with open(os.path.join(DATA, "categories.json"), encoding="utf-8-sig") as f:
    categories = json.load(f)

cat_map   = {c["slug"]: c for c in categories}
works_by_cat = {}
for w in works:
    works_by_cat.setdefault(w["category"], []).append(w)

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

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
    n = abs(n) % 100
    n1 = n % 10
    if 10 < n < 20: return f5
    if 1 < n1 < 5: return f2
    if n1 == 1: return f1
    return f5

# ── Common HTML parts ─────────────────────────

THEME_INIT = """<script>
(function(){
  var t=localStorage.getItem('dimsonsgfx-theme')||
    (window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');
  document.documentElement.setAttribute('data-theme',t);
  document.addEventListener('DOMContentLoaded',function(){document.body.setAttribute('data-theme',t);});
})();
</script>"""

FONTS_LINK = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&family=Rubik:wght@300;400;500&display=swap&subset=cyrillic" rel="stylesheet">'

def nav_items(active_cat=None):
    items = ['<li><a href="/">Главная</a></li>']
    for c in categories:
        act = ' class="active"' if c["slug"] == active_cat else ""
        items.append(f'<li{act}><a href="/category/{c["slug"]}/">{esc(c["label"])}</a></li>')
    return "\n\t\t\t\t".join(items)

def side_nav(active_cat=None):
    items = ['<li><a href="/">Главная</a></li>']
    for c in categories:
        act = " active" if c["slug"] == active_cat else ""
        items.append(f'<li class="{act}"><a href="/category/{c["slug"]}/">{esc(c["icon"])} {esc(c["label"])}</a></li>')
    return "\n\t\t\t\t\t\t".join(items)

def head_html(title, desc, og_img, canonical, extra_schema=""):
    return f"""<!DOCTYPE html>
<html lang="ru">
{THEME_INIT}
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<title>{esc(title)}</title>
\t<meta name="description" content="{esc(desc)}">

\t<!-- Open Graph -->
\t<meta property="og:title" content="{esc(title)}">
\t<meta property="og:description" content="{esc(desc)}">
\t<meta property="og:image" content="{esc(og_img)}">
\t<meta property="og:url" content="{esc(canonical)}">
\t<meta property="og:type" content="website">
\t<meta property="og:locale" content="ru_RU">

\t<!-- Twitter Card -->
\t<meta name="twitter:card" content="summary_large_image">
\t<meta name="twitter:title" content="{esc(title)}">
\t<meta name="twitter:image" content="{esc(og_img)}">

\t<link rel="canonical" href="{esc(canonical)}">
\t<link rel="shortcut icon" href="/assets/images/favicon.png" type="image/png">
\t<meta name="theme-color" content="#f5f6f8">

\t{FONTS_LINK}
\t<link href="/assets/css/styles.css" type="text/css" rel="stylesheet">
\t<link href="/assets/css/patch.css" type="text/css" rel="stylesheet">
{extra_schema}
</head>"""

def header_html(active_cat=None):
    return f"""
\t<div class="wrap-main wrap-center">

\t\t<header class="header fx-row fx-middle">
\t\t\t<a href="/" class="logo"><img src="/assets/images/logo.png" alt="DIMSONSGFX"></a>
\t\t\t<ul class="header-menu fx-row fx-start fx-1 to-mob">
\t\t\t\t{nav_items(active_cat)}
\t\t\t</ul>
\t\t\t<div class="search-btn js-search anim"><span class="far fa-search"></span></div>
\t\t\t<button class="theme-toggle-btn" id="themeToggle" aria-label="Переключить тему" title="Переключить тему">☀️</button>
\t\t\t<div class="btn-menu"><span class="far fa-bars"></span></div>
\t\t</header>

\t\t<!-- END HEADER -->"""

def sidebar_left_html(active_cat=None):
    return f"""
\t\t\t<aside class="col-left fx-first">
\t\t\t\t<div class="side-box to-mob">
\t\t\t\t\t<div class="side-bt title">Навигация</div>
\t\t\t\t\t<ul class="header-menu side-menu">
\t\t\t\t\t\t{side_nav(active_cat)}
\t\t\t\t\t</ul>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Выбор редакции</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" id="sidebar-editor-pick">
\t\t\t\t\t\t<!-- Загружается через JS из works.json -->
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Топ работ</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" data-sidebar="top" data-limit="9">
\t\t\t\t\t\t<!-- Загружается через JS -->
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</aside>

\t\t\t<!-- END COL-LEFT -->"""

def sidebar_right_html():
    return f"""
\t\t\t<aside class="col-right">
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Популярное</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" data-sidebar="top" data-limit="6">
\t\t\t\t\t\t<!-- Загружается через JS -->
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Рекомендуем</div>
\t\t\t\t\t<div class="side-bc mb-remove-30" id="sidebar-recommend">
\t\t\t\t\t\t<!-- Загружается через JS -->
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="side-box">
\t\t\t\t\t<div class="side-bt title">Категории</div>
\t\t\t\t\t<div class="side-bc">
\t\t\t\t\t\t<ul class="side-menu header-menu">
\t\t\t\t\t\t\t{''.join(f"""<li><a href="/category/{c["slug"]}/">{esc(c["icon"])} {esc(c["label"])} <small style="color:#888">({len(works_by_cat.get(c["slug"],[]))})</small></a></li>""" for c in categories)}
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</aside>

\t\t\t<!-- END COL-RIGHT -->"""

def mobile_panel_html(active_cat=None):
    return f"""
\t\t<!-- Mobile side panel -->
\t\t<div class="close-overlay"></div>
\t\t<div class="btn-close"><span class="far fa-times"></span></div>
\t\t<div class="side-panel">
\t\t\t<ul class="header-menu side-menu">
\t\t\t\t{nav_items(active_cat)}
\t\t\t</ul>
\t\t</div>"""

def search_html():
    return """
\t<div class="search-wrap hidden" id="searchWrap">
\t\t<div class="search-header fx-row fx-middle">
\t\t\t<div class="search-title title">Поиск</div>
\t\t\t<div class="search-close"><span class="far fa-times"></span></div>
\t\t</div>
\t\t<form id="quicksearch" method="get" action="/search/">
\t\t\t<div class="search-box">
\t\t\t\t<input id="story" name="q" placeholder="Поиск по сайту..." type="text" autocomplete="off">
\t\t\t\t<button type="submit"><span class="far fa-search"></span></button>
\t\t\t</div>
\t\t</form>
\t</div>"""

def footer_html():
    return f"""
\t\t<footer class="footer fx-row fx-middle">
\t\t\t<div class="footer-copyright fx-1">© 2026 DIMSONSGFX. Все права защищены.</div>
\t\t</footer>

\t\t<!-- END FOOTER -->

\t\t</div>

\t\t<!-- END WRAP-MAIN -->

\t</div>

\t<!-- END WRAP -->

{search_html()}

\t<button id="gotop" aria-label="Наверх"><span class="far fa-arrow-up"></span></button>

\t<script src="/assets/js/libs.js"></script>
\t<script src="/assets/js/site.js"></script>"""

# ── Short item card (like shortstory.tpl) ─────
def short_item(work):
    img_html = ""
    if work.get("thumb"):
        img_html = f'<img src="{esc(work["thumb"])}" alt="{esc(work["title"])}" loading="lazy" width="400" height="280">'
    else:
        img_html = f'<div class="no-image-placeholder"><span class="emoji">{work.get("emoji","🎨")}</span></div>'
    
    cat = cat_map.get(work["category"], {})
    date_str = fmt_date(work.get("date",""))
    desc = (work.get("description","") or "")[:140]
    if len(work.get("description","")) > 140:
        desc += "…"

    return f"""
<div class="short-item" itemscope itemtype="https://schema.org/CreativeWork">
\t<a class="short-link" href="/works/{esc(work['slug'])}/">
\t\t<div class="short-img img-resp img-fit">
\t\t\t{img_html}
\t\t\t<div class="short-category">{esc(cat.get("label", work["category"]))}</div>
\t\t</div>
\t\t<div class="short-title title anim" itemprop="name">{esc(work['title'])}</div>
\t</a>
\t<div class="short-meta fx-row fx-middle icon-left">
\t\t<div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt"></span><time datetime="{esc(work.get('date',''))}">{date_str}</time></div>
\t\t<div class="short-meta-item"><span class="far fa-eye"></span>{work.get("views",0)}</div>
\t</div>
\t<div class="short-text" itemprop="description">{esc(desc)}</div>
\t<div class="short-bottom fx-row fx-middle icon-left">
\t\t<div class="fx-1"></div>
\t\t<a class="short-btn btn" href="/works/{esc(work['slug'])}/">Подробнее</a>
\t</div>
</div>"""

# ── Pagination ────────────────────────────────
def pagination_html(current, total, base_url):
    if total <= 1:
        return ""
    pages = []
    for i in range(1, total+1):
        url = base_url if i == 1 else f"{base_url}page/{i}/"
        if i == current:
            pages.append(f'<li><span>{i}</span></li>')
        else:
            pages.append(f'<li><a href="{url}">{i}</a></li>')
    if current < total:
        next_url = base_url if current+1==1 else f"{base_url}page/{current+1}/"
        pages.append(f'<li><a href="{next_url}">Следующая →</a></li>')
    return f"""
<div class="bottom-nav clr" id="bottom-nav">
\t<div class="pagi-nav clearfix">
\t\t<nav class="navigation" aria-label="Пагинация">
\t\t\t<ul class="pagination">{''.join(pages)}</ul>
\t\t</nav>
\t</div>
</div>"""

# ── Generate SVG placeholders ─────────────────
IMG_DIR = os.path.join(BASE, "assets", "images")
os.makedirs(IMG_DIR, exist_ok=True)

SVG_CARD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <pattern id="p" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0L0 0L0 40" fill="none" stroke="{ac}" stroke-width="0.3" opacity="0.15"/>
    </pattern>
  </defs>
  <rect width="800" height="560" fill="url(#g)"/>
  <rect width="800" height="560" fill="url(#p)"/>
  <circle cx="400" cy="260" r="130" fill="none" stroke="{ac}" stroke-width="1" opacity="0.2"/>
  <text x="400" y="240" font-size="64" text-anchor="middle" dominant-baseline="middle" font-family="Segoe UI Emoji,Apple Color Emoji,sans-serif">{emoji}</text>
  <text x="400" y="310" font-size="20" font-weight="600" text-anchor="middle" fill="{ac}" font-family="system-ui,sans-serif" opacity="0.9">{title}</text>
  <rect x="295" y="335" width="210" height="28" rx="14" fill="{ac}" opacity="0.1"/>
  <text x="400" y="353" font-size="12" text-anchor="middle" fill="{ac}" font-family="system-ui,sans-serif" opacity="0.8">{cat}</text>
  <rect x="16" y="16" width="36" height="2" fill="{ac}" opacity="0.35"/>
  <rect x="16" y="16" width="2" height="36" fill="{ac}" opacity="0.35"/>
  <rect x="748" y="16" width="36" height="2" fill="{ac}" opacity="0.35"/>
  <rect x="782" y="16" width="2" height="36" fill="{ac}" opacity="0.35"/>
  <rect x="16" y="542" width="36" height="2" fill="{ac}" opacity="0.35"/>
  <rect x="16" y="506" width="2" height="36" fill="{ac}" opacity="0.35"/>
  <rect x="748" y="542" width="36" height="2" fill="{ac}" opacity="0.35"/>
  <rect x="782" y="506" width="2" height="36" fill="{ac}" opacity="0.35"/>
</svg>"""

PLACEHOLDERS = [
    # slug,           bg1,       bg2,       accent,    emoji, title,                cat
    ("arts-1",       "#1a1a2e","#0f0f20","#c8a96e","🌆","Urban Dreams",      "Арты"),
    ("arts-2",       "#0d2818","#071510","#4ecca3","🌿","Neon Forest",        "Арты"),
    ("arts-3",       "#0a0a1a","#060610","#7c6fcd","🚀","Cosmic Voyage",      "Арты"),
    ("arts-4",       "#001525","#000d18","#0088cc","🌊","Deep Sea",           "Арты"),
    ("logos-1",      "#1a1a1a","#111111","#c8a96e","◎","Minimalist Mark",    "Логотипы"),
    ("logos-2",      "#1a0a0a","#110606","#cc4444","🐻","The Beast Co.",      "Логотипы"),
    ("logos-3",      "#1a0f08","#110a05","#c87941","☕","Brew & Soul",        "Логотипы"),
    ("logos-4",      "#0a1020","#060b15","#4488ff","⬡","Nexus Labs",         "Логотипы"),
    ("banners-1",    "#1a1500","#110e00","#ffcc00","☀️","Summer Sale 2026",  "Баннеры"),
    ("banners-2",    "#050510","#030308","#8855ff","🎤","Night Conference",   "Баннеры"),
    ("banners-3",    "#001a10","#00100a","#00cc77","📱","App Launch",         "Баннеры"),
    ("illustrations-1","#1a2a10","#101a09","#88cc44","🦊","Лесные истории","Иллюстрации"),
    ("illustrations-2","#0a1020","#060b15","#4499ff","🧠","Digital Minds",  "Иллюстрации"),
    ("illustrations-3","#1a0a20","#110615","#cc44aa","🎭","Faceless",        "Иллюстрации"),
    ("other-1",      "#201505","#150e03","#cc9944","🗺️","Treasure Map",     "Прочее"),
    ("other-2",      "#0a1a20","#060f15","#44aacc","🔷","Aztec Pattern",     "Прочее"),
    ("other-3",      "#050a10","#03060a","#3388ff","📊","Analytics Dashboard","Прочее"),
]

def darken(h, f=0.55):
    h = h.lstrip('#')
    r,g,b = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    return '#{:02x}{:02x}{:02x}'.format(int(r*f*255),int(g*f*255),int(b*f*255))

for slug, c1, c2, ac, emoji, title, cat in PLACEHOLDERS:
    c2d = darken(c1)
    svg = SVG_CARD.format(c1=c1, c2=c2d, ac=ac, emoji=emoji, title=title, cat=cat)
    with open(os.path.join(IMG_DIR, f"placeholder-{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# OG image
og_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#22272e"/>
  <defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0L0 0L0 40" fill="none" stroke="#36c537" stroke-width="0.4" opacity="0.08"/>
  </pattern></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="600" cy="315" r="200" fill="none" stroke="#36c537" stroke-width="1" opacity="0.12"/>
  <text x="600" y="280" font-size="52" font-weight="800" text-anchor="middle" fill="#f0f0f0" font-family="system-ui,sans-serif">DIMSONSGFX</text>
  <text x="600" y="345" font-size="22" text-anchor="middle" fill="#36c537" font-family="system-ui,sans-serif">Портфолио · Арты · Логотипы · Иллюстрации</text>
  <text x="600" y="400" font-size="16" text-anchor="middle" fill="#666" font-family="system-ui,sans-serif">dimsonsgfx.github.io</text>
</svg>"""
with open(os.path.join(IMG_DIR, "og-default.svg"), "w", encoding="utf-8") as f:
    f.write(og_svg)

# Logo SVG (если нет png — используем svg)
logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 60" width="280" height="60">
  <text x="0" y="44" font-size="36" font-weight="800" fill="#010101" font-family="Montserrat,system-ui,sans-serif">DIMSONS<tspan fill="#36c537">GFX</tspan></text>
</svg>"""
# Save logo only if logo.png doesn't exist
logo_png = os.path.join(IMG_DIR, "logo.png")
logo_svg_path = os.path.join(IMG_DIR, "logo.svg")
if not os.path.exists(logo_png):
    with open(logo_svg_path, "w", encoding="utf-8") as f:
        f.write(logo_svg)
    print("Created: logo.svg (fallback)")

print(f"Placeholders: {len(PLACEHOLDERS)} SVGs + og-default.svg")

# ── DATA: works.json ──────────────────────────
WORKS = [
  {"slug":"urban-dreams","title":"Urban Dreams","description":"Городской пейзаж в стиле ретро-футуризм, неоновые огни и дождливые улицы","category":"arts","categoryLabel":"Арты","date":"2026-09-20","image":"/assets/images/placeholder-arts-1.svg","thumb":"/assets/images/placeholder-arts-1.svg","emoji":"🌆","tags":["иллюстрация","город","ретро"],"views":142,"source":"manual"},
  {"slug":"neon-forest","title":"Neon Forest","description":"Фантастический лес с биолюминесцентными растениями и туманом","category":"arts","categoryLabel":"Арты","date":"2026-09-15","image":"/assets/images/placeholder-arts-2.svg","thumb":"/assets/images/placeholder-arts-2.svg","emoji":"🌿","tags":["природа","фэнтези","свет"],"views":98,"source":"manual"},
  {"slug":"cosmic-voyage","title":"Cosmic Voyage","description":"Путешествие сквозь галактику — абстрактная цифровая живопись","category":"arts","categoryLabel":"Арты","date":"2026-09-10","image":"/assets/images/placeholder-arts-3.svg","thumb":"/assets/images/placeholder-arts-3.svg","emoji":"🚀","tags":["космос","абстракция","цифровое"],"views":201,"source":"manual"},
  {"slug":"deep-sea","title":"Deep Sea","description":"Загадочные глубины океана, светящиеся медузы и морские существа","category":"arts","categoryLabel":"Арты","date":"2026-09-05","image":"/assets/images/placeholder-arts-4.svg","thumb":"/assets/images/placeholder-arts-4.svg","emoji":"🌊","tags":["море","фэнтези"],"views":77,"source":"manual"},
  {"slug":"logo-minimalist","title":"Minimalist Mark","description":"Логотип для студии дизайна — чистые линии, золотое сечение","category":"logos","categoryLabel":"Логотипы","date":"2026-09-18","image":"/assets/images/placeholder-logos-1.svg","thumb":"/assets/images/placeholder-logos-1.svg","emoji":"◎","tags":["минимализм","геометрия","брендинг"],"views":315,"source":"manual"},
  {"slug":"logo-beast","title":"The Beast Co.","description":"Агрессивный логотип для спортивного бренда — медведь в геометрическом стиле","category":"logos","categoryLabel":"Логотипы","date":"2026-09-12","image":"/assets/images/placeholder-logos-2.svg","thumb":"/assets/images/placeholder-logos-2.svg","emoji":"🐻","tags":["спорт","животное","геометрия"],"views":189,"source":"manual"},
  {"slug":"logo-coffee","title":"Brew & Soul","description":"Уютный логотип для кофейни с ручной типографикой и паром","category":"logos","categoryLabel":"Логотипы","date":"2026-09-08","image":"/assets/images/placeholder-logos-3.svg","thumb":"/assets/images/placeholder-logos-3.svg","emoji":"☕","tags":["кофе","типографика","уют"],"views":94,"source":"manual"},
  {"slug":"logo-tech","title":"Nexus Labs","description":"Современный логотип для IT-стартапа — сети, узлы, соединения","category":"logos","categoryLabel":"Логотипы","date":"2026-09-02","image":"/assets/images/placeholder-logos-4.svg","thumb":"/assets/images/placeholder-logos-4.svg","emoji":"⬡","tags":["технологии","минимализм"],"views":122,"source":"manual"},
  {"slug":"banner-sale","title":"Summer Sale 2026","description":"Анимированный баннер для интернет-магазина, летняя акция","category":"banners","categoryLabel":"Баннеры","date":"2026-09-22","image":"/assets/images/placeholder-banners-1.svg","thumb":"/assets/images/placeholder-banners-1.svg","emoji":"☀️","tags":["реклама","акция","анимация"],"views":267,"source":"manual"},
  {"slug":"banner-event","title":"Night Conference","description":"Баннер для онлайн-конференции, тёмная тема с частицами","category":"banners","categoryLabel":"Баннеры","date":"2026-09-16","image":"/assets/images/placeholder-banners-2.svg","thumb":"/assets/images/placeholder-banners-2.svg","emoji":"🎤","tags":["конференция","тёмная тема"],"views":88,"source":"manual"},
  {"slug":"banner-app","title":"App Launch","description":"Промо-баннер для запуска мобильного приложения","category":"banners","categoryLabel":"Баннеры","date":"2026-09-11","image":"/assets/images/placeholder-banners-3.svg","thumb":"/assets/images/placeholder-banners-3.svg","emoji":"📱","tags":["мобайл","запуск","промо"],"views":156,"source":"manual"},
  {"slug":"children-book","title":"Лесные истории","description":"Иллюстрации для детской книги — добрые персонажи и сказочный лес","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-19","image":"/assets/images/placeholder-illustrations-1.svg","thumb":"/assets/images/placeholder-illustrations-1.svg","emoji":"🦊","tags":["детская","книга","персонажи"],"views":203,"source":"manual"},
  {"slug":"editorial-tech","title":"Digital Minds","description":"Редакционная иллюстрация о влиянии технологий на человека","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-14","image":"/assets/images/placeholder-illustrations-2.svg","thumb":"/assets/images/placeholder-illustrations-2.svg","emoji":"🧠","tags":["редакционная","технологии"],"views":67,"source":"manual"},
  {"slug":"portrait-abstract","title":"Faceless","description":"Абстрактный портрет — разложение образа на геометрические формы","category":"illustrations","categoryLabel":"Иллюстрации","date":"2026-09-09","image":"/assets/images/placeholder-illustrations-3.svg","thumb":"/assets/images/placeholder-illustrations-3.svg","emoji":"🎭","tags":["портрет","геометрия","абстракция"],"views":144,"source":"manual"},
  {"slug":"map-treasure","title":"Treasure Map","description":"Стилизованная карта сокровищ — пиратская тематика и старинный пергамент","category":"other","categoryLabel":"Прочее","date":"2026-09-17","image":"/assets/images/placeholder-other-1.svg","thumb":"/assets/images/placeholder-other-1.svg","emoji":"🗺️","tags":["карта","пираты"],"views":55,"source":"manual"},
  {"slug":"pattern-aztec","title":"Aztec Pattern","description":"Орнаментальный паттерн в ацтекском стиле для текстиля","category":"other","categoryLabel":"Прочее","date":"2026-09-13","image":"/assets/images/placeholder-other-2.svg","thumb":"/assets/images/placeholder-other-2.svg","emoji":"🔷","tags":["паттерн","орнамент"],"views":81,"source":"manual"},
  {"slug":"ui-dashboard","title":"Analytics Dashboard","description":"UI-дизайн дашборда аналитики — тёмная тема, графики, карточки","category":"other","categoryLabel":"Прочее","date":"2026-09-07","image":"/assets/images/placeholder-other-3.svg","thumb":"/assets/images/placeholder-other-3.svg","emoji":"📊","tags":["UI","дашборд"],"views":119,"source":"manual"},
]

CATEGORIES = [
  {"slug":"arts","label":"Арты","icon":"🎨","description":"Цифровые арты, концепт-арт и авторские иллюстрации"},
  {"slug":"logos","label":"Логотипы","icon":"✦","description":"Разработка логотипов и визуальной идентичности для брендов"},
  {"slug":"banners","label":"Баннеры","icon":"🖼","description":"Рекламные баннеры, промо-материалы и визуальный контент"},
  {"slug":"illustrations","label":"Иллюстрации","icon":"✏️","description":"Редакционные иллюстрации, детские книги, персонажи"},
  {"slug":"other","label":"Прочее","icon":"💎","description":"Паттерны, UI-дизайн, карты, текстуры и разное"},
]

with open(os.path.join(DATA, "works.json"), "w", encoding="utf-8") as f:
    json.dump(WORKS, f, ensure_ascii=False, indent=2)
with open(os.path.join(DATA, "categories.json"), "w", encoding="utf-8") as f:
    json.dump(CATEGORIES, f, ensure_ascii=False, indent=2)
print("Data files written")

# Re-load for generation
works = WORKS
categories = CATEGORIES
cat_map   = {c["slug"]: c for c in categories}
works_by_cat = {}
for w in works:
    works_by_cat.setdefault(w["category"], []).append(w)

# ── INDEX PAGE ────────────────────────────────
sorted_works = sorted(works, key=lambda w: w.get("date",""), reverse=True)

# Latest 8 on homepage
recent = sorted_works[:8]
recent_cards = "\n".join(short_item(w) for w in recent)
all_cards = "\n".join(short_item(w) for w in sorted_works)

# Category pills
pills = "".join(
    f'<a href="/category/{c["slug"]}/" class="cat-pill">{esc(c["icon"])} {esc(c["label"])} <span class="pill-cnt">({len(works_by_cat.get(c["slug"],[]))})</span></a>\n\t\t\t\t'
    for c in categories
)

index_schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfilePage","name":"DIMSONSGFX — Портфолио","url":"https://dimsonsgfx.github.io/","description":"Портфолио цифрового художника: арты, логотипы, баннеры, иллюстрации"}
</script>"""

index_html = head_html(
    "DIMSONSGFX — Портфолио цифрового художника",
    "Портфолио цифрового художника: арты, логотипы, баннеры, иллюстрации. Авторские работы в разных стилях.",
    f"{SITE_URL}/assets/images/og-default.svg",
    f"{SITE_URL}/",
    index_schema
) + f"""
<body>
<div class="wrap">
{header_html()}

\t\t<div class="content fx-row fx-start">

\t\t\t<main class="col-main">
\t\t\t\t<div class="sect">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<div class="sect-title title fx-1">Последние работы</div>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content">
\t\t\t\t\t\t{recent_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t<div class="sect" style="margin-top:30px">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<div class="sect-title title fx-1">Все работы</div>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content">
\t\t\t\t\t\t{all_cards}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</main>

\t\t\t<!-- END COL-MAIN -->

{sidebar_left_html()}
{sidebar_right_html()}

\t\t</div>

\t\t<!-- END CONTENT -->

\t\t<!-- SEO -->
\t\t<div class="site-desc">
\t\t\t<h1>DIMSONSGFX — портфолио цифрового художника</h1>
\t\t\t<p>Добро пожаловать в моё портфолио! Здесь вы найдёте цифровые арты, логотипы, баннеры и иллюстрации.</p>
\t\t</div>

{footer_html()}
{mobile_panel_html()}
</div>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("Generated: index.html")

# ── CATEGORY PAGES ────────────────────────────
PER_PAGE = 12

for cat in categories:
    slug = cat["slug"]
    label = cat["label"]
    desc = cat["description"]
    icon = cat["icon"]
    cat_works = sorted(works_by_cat.get(slug, []), key=lambda w: w.get("date",""), reverse=True)
    count = len(cat_works)
    
    total_pages = max(1, (count + PER_PAGE - 1) // PER_PAGE)
    
    for page_num in range(1, total_pages + 1):
        page_works = cat_works[(page_num-1)*PER_PAGE : page_num*PER_PAGE]
        cards = "\n".join(short_item(w) for w in page_works)
        
        if page_num == 1:
            out_dir = os.path.join(BASE, "category", slug)
            canonical = f"{SITE_URL}/category/{slug}/"
        else:
            out_dir = os.path.join(BASE, "category", slug, "page", str(page_num))
            canonical = f"{SITE_URL}/category/{slug}/page/{page_num}/"
        
        os.makedirs(out_dir, exist_ok=True)
        
        og_img = f"{SITE_URL}/assets/images/og-default.svg"
        if page_works and page_works[0].get("thumb"):
            og_img = f"{SITE_URL}{page_works[0]['thumb']}"
        
        page_title = f"{label} — DIMSONSGFX" if page_num == 1 else f"{label} — стр. {page_num} — DIMSONSGFX"
        meta_desc = f"{desc}. {count} {pluralRu(count)} в портфолио."
        
        schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"{esc(page_title)}","url":"{esc(canonical)}","description":"{esc(meta_desc)}"}}
</script>"""
        
        pagi = pagination_html(page_num, total_pages, f"{SITE_URL}/category/{slug}/")
        
        cat_html = head_html(page_title, meta_desc, og_img, canonical, schema) + f"""
<body>
<div class="wrap">
{header_html(slug)}

\t\t<div class="content fx-row fx-start">

\t\t\t<main class="col-main">
\t\t\t\t<div class="sect">
\t\t\t\t\t<div class="sect-header">
\t\t\t\t\t\t<div class="sect-title title fx-1">{esc(icon)} {esc(label)}</div>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="sect-content" id="dle-content">
\t\t\t\t\t\t{cards if cards else '<p style="color:#888;padding:30px 0">Работы появятся здесь совсем скоро</p>'}
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t{pagi}
\t\t\t</main>

\t\t\t<!-- END COL-MAIN -->

{sidebar_left_html(slug)}
{sidebar_right_html()}

\t\t</div>

\t\t<!-- END CONTENT -->

{footer_html()}
{mobile_panel_html(slug)}
</div>
</body>
</html>"""
        
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(cat_html)
    
    print(f"Category: /category/{slug}/ ({total_pages} pages, {count} works)")

# ── WORK DETAIL PAGES ─────────────────────────
for w in works:
    slug = w["slug"]
    cat_slug = w["category"]
    cat = cat_map.get(cat_slug, {"label": cat_slug, "icon":"🎨"})
    cat_label = cat["label"]
    cat_icon  = cat.get("icon","🎨")
    
    date_str = fmt_date(w.get("date",""))
    img_src  = w.get("image","")
    og_img   = f"{SITE_URL}{img_src}" if img_src and not img_src.startswith("http") else f"{SITE_URL}/assets/images/og-default.svg"
    canonical = f"{SITE_URL}/works/{slug}/"
    tags = w.get("tags",[])
    
    img_html = ""
    if img_src:
        img_html = f'<img src="{esc(img_src)}" alt="{esc(w["title"])}" loading="lazy" width="800" height="560" style="width:100%;height:auto;border-radius:4px;margin-bottom:30px;">'
    else:
        img_html = f'<div style="height:400px;background:#e8eaed;display:flex;align-items:center;justify-content:center;font-size:6rem;margin-bottom:30px;border-radius:4px;">{w.get("emoji","🎨")}</div>'
    
    tags_html = ""
    if tags:
        tags_html = f'<div class="ftags"><span class="far fa-tags"></span>'
        tags_html += " ".join(f'<a href="/search/?q={esc(t)}">{esc(t)}</a>' for t in tags)
        tags_html += '</div>'
    
    # Related works
    related = [rw for rw in works if rw["category"] == cat_slug and rw["slug"] != slug][:3]
    related_html = ""
    if related:
        related_cards = "\n".join(short_item(rw) for rw in related)
        related_html = f"""
\t\t<div class="sect side-box frels ignore-select">
\t\t\t<div class="sect-header fx-row fx-middle">
\t\t\t\t<div class="sect-title fx-1 title">Читайте также:</div>
\t\t\t</div>
\t\t\t<div class="sect-content fx-row mb-remove-30" id="dle-content">
\t\t\t\t{related_cards}
\t\t\t</div>
\t\t</div>"""
    
    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CreativeWork","name":"{esc(w['title'])}","description":"{esc(w.get('description',''))}","dateCreated":"{esc(w.get('date',''))}","url":"{esc(canonical)}","image":"{esc(og_img)}","genre":"{esc(cat_label)}"}}
</script>"""
    
    work_html = head_html(
        f"{w['title']} — DIMSONSGFX",
        w.get("description",""),
        og_img,
        canonical,
        schema
    ) + f"""
<body>
<div class="wrap">
{header_html(cat_slug)}

\t\t<div class="content fx-row fx-start">

\t\t\t<main class="col-main">
\t\t\t\t<article class="article" itemscope itemtype="https://schema.org/CreativeWork">

\t\t\t\t<div class="fmain side-box">
\t\t\t\t\t<!-- Breadcrumb -->
\t\t\t\t\t<div style="font-size:13px;color:#888;margin-bottom:15px;">
\t\t\t\t\t\t<a href="/">Главная</a> › <a href="/category/{esc(cat_slug)}/">{esc(cat_label)}</a> › {esc(w['title'])}
\t\t\t\t\t</div>
\t\t\t\t\t<h1 class="sect-title" itemprop="name">{esc(w['title'])}</h1>
\t\t\t\t\t<div class="short-meta fx-row fx-middle icon-left">
\t\t\t\t\t\t<div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt"></span><time datetime="{esc(w.get('date',''))}" itemprop="dateCreated">{date_str}</time></div>
\t\t\t\t\t\t<div class="short-meta-item"><span class="far fa-eye"></span>{w.get('views',0)}</div>
\t\t\t\t\t\t<div class="short-meta-item"><a href="/category/{esc(cat_slug)}/" itemprop="genre">{cat_icon} {esc(cat_label)}</a></div>
\t\t\t\t\t</div>
\t\t\t\t\t{img_html}
\t\t\t\t\t<div class="ftext full-text clearfix" itemprop="description">
\t\t\t\t\t\t<p>{esc(w.get('description',''))}</p>
\t\t\t\t\t</div>
\t\t\t\t\t{tags_html}
\t\t\t\t\t<div class="fbtm fx-row fx-middle ignore-select fbtm-one">
\t\t\t\t\t\t<div class="fx-1"></div>
\t\t\t\t\t\t<a href="/category/{esc(cat_slug)}/" class="btn">← Назад к {esc(cat_label)}</a>
\t\t\t\t\t</div>
\t\t\t\t</div>

\t\t\t\t{related_html}

\t\t\t\t</article>
\t\t\t</main>

\t\t\t<!-- END COL-MAIN -->

{sidebar_left_html(cat_slug)}
{sidebar_right_html()}

\t\t</div>

\t\t<!-- END CONTENT -->

{footer_html()}
{mobile_panel_html(cat_slug)}
</div>
</body>
</html>"""
    
    out_dir = os.path.join(BASE, "works", slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(work_html)

print(f"Works: {len(works)} detail pages")

# ── SEARCH PAGE ───────────────────────────────
search_html_page = head_html(
    "Поиск — DIMSONSGFX",
    "Поиск по портфолио DIMSONSGFX",
    f"{SITE_URL}/assets/images/og-default.svg",
    f"{SITE_URL}/search/"
) + f"""
<body>
<div class="wrap">
{header_html()}

\t\t<div class="content fx-row fx-start">

\t\t\t<main class="col-main">
\t\t\t\t<div class="side-box">
\t\t\t\t\t<h1 class="mtitle">Поиск</h1>
\t\t\t\t\t<form id="searchForm" style="margin-bottom:30px">
\t\t\t\t\t\t<div class="search-box" style="position:relative">
\t\t\t\t\t\t\t<input type="text" id="searchInput" name="q" placeholder="Введите запрос..." style="width:100%;height:44px;padding:0 50px 0 15px;border:1px solid #e3e3e3;border-radius:4px;font-size:16px">
\t\t\t\t\t\t\t<button type="submit" style="position:absolute;right:5px;top:2px;background:transparent;border:none;font-size:18px;cursor:pointer;color:#36c537;height:40px;width:40px"><span class="far fa-search"></span></button>
\t\t\t\t\t\t</div>
\t\t\t\t\t</form>
\t\t\t\t\t<div id="searchResults" class="fx-row" id="dle-content"></div>
\t\t\t\t</div>
\t\t\t</main>

\t\t\t<!-- END COL-MAIN -->

{sidebar_left_html()}
{sidebar_right_html()}

\t\t</div>

{footer_html()}
{mobile_panel_html()}
</div>
<script>
document.addEventListener('DOMContentLoaded', async () => {{
  const params = new URLSearchParams(window.location.search);
  const q = params.get('q') || '';
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  if (input) input.value = q;
  
  if (!q) return;
  
  const works = await loadWorks();
  const ql = q.toLowerCase();
  const found = works.filter(w =>
    w.title.toLowerCase().includes(ql) ||
    (w.description||'').toLowerCase().includes(ql) ||
    (w.tags||[]).some(t => t.toLowerCase().includes(ql)) ||
    (w.categoryLabel||'').toLowerCase().includes(ql)
  );
  
  if (!found.length) {{
    results.innerHTML = '<p style="color:#888;padding:20px 0">По запросу <strong>' + esc(q) + '</strong> ничего не найдено</p>';
    return;
  }}
  
  results.innerHTML = found.map(w => renderShortItem(w)).join('');
  initLazyLoad();
  
  document.getElementById('searchForm').addEventListener('submit', e => {{
    e.preventDefault();
    const nq = input.value.trim();
    if (nq) window.location.href = '/search/?q=' + encodeURIComponent(nq);
  }});
}});
</script>
</body>
</html>"""

os.makedirs(os.path.join(BASE, "search"), exist_ok=True)
with open(os.path.join(BASE, "search", "index.html"), "w", encoding="utf-8") as f:
    f.write(search_html_page)
print("Search: /search/")

# ── 404 PAGE ──────────────────────────────────
page_404 = head_html(
    "404 — Страница не найдена · DIMSONSGFX",
    "Страница не найдена",
    f"{SITE_URL}/assets/images/og-default.svg",
    f"{SITE_URL}/404.html"
) + f"""
<body>
<div class="wrap">
{header_html()}

\t\t<div class="content fx-row fx-start">
\t\t\t<main class="col-main">
\t\t\t\t<div class="side-box" style="text-align:center;padding:60px 30px">
\t\t\t\t\t<div style="font-size:8rem;font-weight:800;color:#36c537;line-height:1">404</div>
\t\t\t\t\t<p style="color:#888;margin:20px 0 30px;font-size:18px">Страница не найдена</p>
\t\t\t\t\t<a href="/" class="btn">← На главную</a>
\t\t\t\t</div>
\t\t\t</main>
{sidebar_left_html()}
{sidebar_right_html()}
\t\t</div>
{footer_html()}
{mobile_panel_html()}
</div>
</body>
</html>"""

with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
    f.write(page_404)
print("Generated: 404.html")

# ── SITEMAP ───────────────────────────────────
urls = [f'  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>']
for c in categories:
    urls.append(f'  <url><loc>{SITE_URL}/category/{c["slug"]}/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
for w in works:
    urls.append(f'  <url><loc>{SITE_URL}/works/{w["slug"]}/</loc><lastmod>{w.get("date",TODAY)}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(urls) + "\n</urlset>"
with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)
print("Generated: sitemap.xml")

# ── ROBOTS.TXT ────────────────────────────────
robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
with open(os.path.join(BASE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)
print("Generated: robots.txt")

# ── GitHub Pages CNAME / nojekyll ─────────────
with open(os.path.join(BASE, ".nojekyll"), "w") as f:
    pass

total_pages = 1 + len(categories) + len(works) + 1 + 1  # index + cats + works + search + 404
print(f"\n✅ Build complete! {total_pages} pages generated.")
print(f"   Works: {len(works)}, Categories: {len(categories)}, SVGs: {len(PLACEHOLDERS)+1}")
