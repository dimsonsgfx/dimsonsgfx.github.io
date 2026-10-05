#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync GFxtra RSS to Telegram Channel (@dimsonsgfx) and GitHub Pages Site.
100% Serverless - Runs locally or via GitHub Actions.
"""

import os
import sys
import json
import re
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SITE_ROOT, "data")
WORKS_DIR = os.path.join(SITE_ROOT, "works")
SYNC_STATE_FILE = os.path.join(DATA_DIR, "synced_rss.json")

import html as html_lib
from urllib.parse import urlparse

DEFAULT_RSS_URLS = [
    "https://www.gfxtra31.com/user/dimsons/news/rss.xml",
    "https://www.desirefx.com/author/herogfx/feed/"
]
DEFAULT_TG_CHANNEL = "@dimsonsgfx"
DEFAULT_TG_TOKEN = "8639708447:AAGXumHk_VfSCF9W9YuYjh2rq7ImceQo_s8"

CATEGORY_MAP = [
    {
        "slug": "video-templates",
        "name": "Video Templates",
        "tag": "VideoTemplates",
        "keywords": ["davinci resolve", "davinci", "after effects", "premiere pro", "premiere", "aep", "mogrt", "drp", "drfx", "video template", "video templates", "motion graphics", "opener"]
    },
    {
        "slug": "fonts",
        "name": "Fonts",
        "tag": "Fonts",
        "keywords": ["font", "fonts", "typeface", "typography", "otf", "ttf", "woff"]
    },
    {
        "slug": "3d-print-models",
        "name": "3D Models",
        "tag": "3DModels",
        "keywords": ["blender", "3d model", "3d models", "cinema 4d", "c4d", "fbx", "obj", "stl", "3d print", "3d assets", "other 3d content", "miniature", "cosplay", "action figure", "print in place"]
    },
    {
        "slug": "indesign-templates",
        "name": "InDesign Templates",
        "tag": "InDesign",
        "keywords": ["indesign", "indd", "idml", "magazine", "brochure", "editorial", "flyer", "lookbook", "annual report"]
    },
    {
        "slug": "powerpoint-templates",
        "name": "PowerPoint Templates",
        "tag": "PowerPoint",
        "keywords": ["powerpoint", "pptx", "keynote", "pitch deck", "presentation", "google slides"]
    },
    {
        "slug": "mockup-templates",
        "name": "Mockup Templates",
        "tag": "Mockup",
        "keywords": ["mockup", "psd mockup", "psdt", "packaging", "branding mockup", "scene generator", "device mockup", "iphone", "t-shirt"]
    },
    {
        "slug": "ui-design-kits",
        "name": "UI Design Kits",
        "tag": "UIDesign",
        "keywords": ["ui kit", "ux", "web design", "figma", "vector", "vectors", "elements", "dashboard", "icon kit", "crypto"]
    }
]


def load_synced_state():
    if os.path.isfile(SYNC_STATE_FILE):
        try:
            with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_synced_state(state):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def detect_category(title, rss_category):
    t_low = title.lower()
    # Priority 1: match title keywords first so title overrides generic RSS category
    for cat in CATEGORY_MAP:
        for kw in cat["keywords"]:
            if kw in t_low:
                return cat
    # Priority 2: match combined title + rss_category
    combined = f"{title} {rss_category}".lower()
    for cat in CATEGORY_MAP:
        for kw in cat["keywords"]:
            if kw in combined:
                return cat
    return CATEGORY_MAP[-1]  # fallback to ui-design-kits


def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    return slug[:60].rstrip('-') if slug else 'item'


def clean_html(raw_html):
    if not raw_html:
        return ""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    # Remove extra spaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def extract_specs(raw_html):
    """Extract format/size specs like 'INDD | 974 MB' or 'PSDT | 1.6 GB' from DLE or WordPress description"""
    if not raw_html:
        return ""
    unescaped = html_lib.unescape(raw_html)
    # Look for <p> blocks or text containing format | size
    for block in re.split(r'</p>|<br\s*/?>|\n', unescaped, flags=re.IGNORECASE):
        text_line = re.sub(r'<[^>]+>', ' ', block).strip()
        text_line = re.sub(r'\s+', ' ', text_line)
        if "|" in text_line and re.search(r'\b(mb|gb|kb|psd|psdt|indd|idml|pptx|ppt|ai|eps|png|otf|ttf|aep|stl|obj)\b', text_line, re.IGNORECASE):
            # Remove trailing download button text if present in plain description
            text_line = re.sub(r'\s*DOWNLOAD\s+WITH\s+.*$', '', text_line, flags=re.IGNORECASE).strip()
            if len(text_line) <= 90:
                return text_line
    match = re.search(r'([A-Za-z0-9\s,\.]+\|[A-Za-z0-9\s,\.]+)', unescaped)
    if match:
        res = re.sub(r'\s*DOWNLOAD\s+WITH\s+.*$', '', match.group(1), flags=re.IGNORECASE).strip()
        return res[:90]
    return ""


def download_image(img_url):
    parsed = urlparse(img_url)
    origin = f"{parsed.scheme}://{parsed.netloc}/" if parsed.scheme and parsed.netloc else "https://www.gfxtra31.com/"
    req = urllib.request.Request(
        img_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": origin
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def send_telegram_photo(token, chat_id, photo_bytes, filename, caption):
    """Send photo to Telegram channel via multipart/form-data."""
    boundary = "----TelegramFormBoundary" + str(int(time.time() * 1000))
    url = f"https://api.telegram.org/bot{token}/sendPhoto"

    body = []
    # chat_id
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8"))
    # caption
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    # parse_mode
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nHTML\r\n".encode("utf-8"))
    # photo file
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{filename}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode("utf-8")
    )
    body.append(photo_bytes)
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    full_payload = b"".join(body)

    req = urllib.request.Request(
        url,
        data=full_payload,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "DimsonsGFX-SyncBot/1.0"
        }
    )

    with urllib.request.urlopen(req, timeout=40) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("ok"):
            return res["result"]["message_id"]
        else:
            raise Exception(f"Telegram API returned not ok: {res}")


def parse_single_rss_page(page_url, base_origin):
    req = urllib.request.Request(
        page_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        content = resp.read()
    root = ET.fromstring(content)
    items = []
    content_ns_tag = "{http://purl.org/rss/1.0/modules/content/}encoded"

    for item in root.findall("channel/item"):
        title = html_lib.unescape((item.findtext("title") or "").strip())
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link).strip()
        cats = [c.text.strip() for c in item.findall("category") if c.text and c.text.strip()]
        category = " ".join(cats)
        pub_date = (item.findtext("pubDate") or "").strip()
        desc_raw = (item.findtext("description") or "").strip()
        content_encoded = (item.findtext(content_ns_tag) or "").strip()
        desc_html = content_encoded if content_encoded else desc_raw

        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', desc_html, re.IGNORECASE)
        if not img_match and desc_raw:
            img_match = re.search(r'src=["\']([^"\']+)["\']', desc_raw, re.IGNORECASE)

        img_url = ""
        if img_match:
            img_src = img_match.group(1).strip()
            if img_src.startswith("/"):
                img_url = base_origin + img_src
            else:
                img_url = img_src

        items.append({
            "title": title,
            "link": link,
            "guid": guid,
            "category": category,
            "pub_date": pub_date,
            "desc_html": desc_html,
            "img_url": img_url
        })
    return items


def parse_rss_feed(feed_url, max_pages=5):
    parsed_feed = urlparse(feed_url)
    base_origin = f"{parsed_feed.scheme}://{parsed_feed.netloc}"
    all_items = parse_single_rss_page(feed_url, base_origin)

    # For WordPress feeds (/feed/), paginate ?paged=2..max_pages so batches >10 posts are never missed
    if "/feed" in parsed_feed.path.lower():
        seen_links = {it["link"] for it in all_items}
        for page_num in range(2, max_pages + 1):
            sep = "&" if "?" in feed_url else "?"
            paged_url = f"{feed_url}{sep}paged={page_num}"
            try:
                page_items = parse_single_rss_page(paged_url, base_origin)
                if not page_items:
                    break
                added = 0
                for it in page_items:
                    if it["link"] not in seen_links:
                        seen_links.add(it["link"])
                        all_items.append(it)
                        added += 1
                if added == 0:
                    break
            except Exception:
                break

    return all_items


def main():
    token = os.environ.get("TG_BOT_TOKEN", DEFAULT_TG_TOKEN).strip()
    channel = os.environ.get("TG_CHANNEL", DEFAULT_TG_CHANNEL).strip()
    env_rss = os.environ.get("RSS_URL", "").strip()
    if env_rss:
        rss_urls = [u.strip() for u in env_rss.split(",") if u.strip()]
        for def_u in DEFAULT_RSS_URLS:
            if def_u not in rss_urls:
                rss_urls.append(def_u)
    else:
        rss_urls = list(DEFAULT_RSS_URLS)

    print(f"=== Starting RSS Sync ===")
    print(f"RSS Sources: {', '.join(rss_urls)}")
    print(f"Target Channel: {channel}")

    synced_items = load_synced_state()
    synced_links = {item if isinstance(item, str) else item.get("link", "") for item in synced_items}
    synced_guids = {item.get("guid", "") for item in synced_items if isinstance(item, dict) and item.get("guid")}
    synced_slugs = {item.get("slug", "") for item in synced_items if isinstance(item, dict) and item.get("slug")}
    print(f"Previously synced items: {len(synced_links)}")

    items = []
    for feed_url in rss_urls:
        try:
            feed_items = parse_rss_feed(feed_url)
            print(f"Found {len(feed_items)} items in RSS feed: {feed_url}")
            items.extend(feed_items)
        except Exception as e:
            print(f"Warning: Error reading RSS feed {feed_url}: {e}")

    if not items:
        print("Error: Could not read any items from RSS feeds.")
        return 1

    # Filter out already synced items (by link, guid, or slug)
    new_items = []
    seen_batch_slugs = set()
    for i in items:
        s = generate_slug(i["title"])
        if i["link"] in synced_links or i["guid"] in synced_links or i["guid"] in synced_guids or s in synced_slugs or s in seen_batch_slugs:
            continue
        seen_batch_slugs.add(s)
        new_items.append(i)

    print(f"New items to sync: {len(new_items)}")

    if not new_items:
        print("Everything is up to date! Checking cloud star ratings...")
        try:
            import subprocess
            build_script = os.path.join(SITE_ROOT, "scripts", "build.py")
            subprocess.run([sys.executable, build_script], check=True)
            subprocess.run(
                ["git", "checkout", "--", "pinterest-feed.xml", "feed.xml", "sitemap.xml", "index.html", "404.html", "dmca/", "search/", "category/"],
                cwd=SITE_ROOT,
                check=False
            )
        except Exception as e:
            print(f"Cloud ratings check skipped: {e}")
        return 0

    # Process items in chronological order (oldest first so latest ends on top)
    new_items.reverse()

    synced_count = 0
    for idx, item in enumerate(new_items, 1):
        title = item["title"]
        link = item["link"]
        cat_info = detect_category(title, item["category"])
        specs = extract_specs(item["desc_html"])
        slug = generate_slug(title)

        print(f"\n[{idx}/{len(new_items)}] Processing: {title}")
        print(f"Category: {cat_info['name']} ({cat_info['slug']})")

        # 1. Download preview image
        photo_bytes = None
        if item["img_url"]:
            try:
                print(f"Downloading image from: {item['img_url']}")
                photo_bytes = download_image(item["img_url"])
            except Exception as e:
                print(f"Warning: Failed to download image: {e}")

        # 2. Prepare Telegram Caption
        channel_name_clean = channel.lstrip("@")
        caption_lines = [
            f"🎨 <b>{title}</b>",
            "",
            f"📁 <b>Category:</b> #{cat_info['tag']} | {cat_info['name']}"
        ]
        if specs:
            caption_lines.append(f"📦 <b>Details:</b> <code>{specs}</code>")

        caption_lines.extend([
            "",
            f"🔗 <b>Download & Source:</b>",
            f"{link}",
            "",
            f"⚡ <a href=\"https://dimsonsgfx.github.io/category/{cat_info['slug']}/\">Browse on DIMSONSGFX</a>"
        ])
        caption = "\n".join(caption_lines)

        # 3. Post to Telegram
        msg_id = None
        if photo_bytes:
            try:
                print(f"Posting photo to Telegram channel {channel}...")
                msg_id = send_telegram_photo(token, channel, photo_bytes, f"{slug}.jpg", caption)
                print(f"Posted to Telegram! Message ID: {msg_id}")
            except urllib.error.HTTPError as he:
                err_body = he.read().decode(errors="ignore") if hasattr(he, "read") else str(he)
                print(f"Telegram HTTP Error {he.code}: {err_body}")
                if he.code == 403:
                    print(f"\n[ATTENTION] The bot is not yet an administrator in {channel}!")
                    print(f"Please add @dimsonsgfx_bot as administrator with 'Post Messages' permission to {channel}.")
                    print("Skipping to prevent missing posts until bot is added.\n")
                    return 1
                raise
            except Exception as e:
                print(f"Telegram posting error: {e}")
                raise
        else:
            print("No image available to post to Telegram.")

        tg_post_url = f"https://t.me/{channel_name_clean}/{msg_id}" if msg_id else f"https://t.me/{channel_name_clean}"

        # 4. Save to local website repository (works/<slug>/post.md)
        work_dir = os.path.join(WORKS_DIR, slug)
        os.makedirs(work_dir, exist_ok=True)

        cover_filename = "cover.jpg"
        if photo_bytes:
            cover_path = os.path.join(work_dir, cover_filename)
            with open(cover_path, "wb") as f:
                f.write(photo_bytes)

        # Determine date
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Tags
        tags = [cat_info["name"].split()[0], "Digital Assets", "Graphic Design"]
        if specs:
            for s in specs.split("|"):
                cleaned = s.strip()
                if cleaned and cleaned not in tags:
                    tags.append(cleaned)

        tags_yaml = ", ".join([f'"{t}"' for t in tags])

        post_md_content = f"""---
title: "{title}"
slug: "{slug}"
date: "{today_str}"
category: "{cat_info['slug']}"
tags: [{tags_yaml}]
cover: "{cover_filename}"
download_url: "{tg_post_url}"
source_url: ""
telegram_post_id: {msg_id if msg_id else 0}
---

### {title}

High-quality creative digital asset collection.

{f'**Technical Details:** {specs}' if specs else ''}

- **Category:** {cat_info['name']}
- **Download:** Available via our official Telegram channel [**@{channel_name_clean}**]({tg_post_url})
"""
        post_md_path = os.path.join(work_dir, "post.md")
        with open(post_md_path, "w", encoding="utf-8") as f:
            f.write(post_md_content)

        # 5. Record state
        synced_items.append({
            "title": title,
            "link": link,
            "guid": item["guid"],
            "slug": slug,
            "telegram_msg_id": msg_id,
            "telegram_url": tg_post_url,
            "synced_at": datetime.now(timezone.utc).isoformat()
        })
        save_synced_state(synced_items)
        synced_count += 1
        time.sleep(2)  # Avoid Telegram rate limits between multiple posts

    print(f"\nSuccessfully synced {synced_count} items to Telegram and website.")

    # 6. Rebuild website
    print("Rebuilding website via build.py...")
    import subprocess
    build_script = os.path.join(SITE_ROOT, "scripts", "build.py")
    subprocess.run([sys.executable, build_script], check=True)
    print("Website rebuild complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
