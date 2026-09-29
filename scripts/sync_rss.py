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

DEFAULT_RSS_URL = "https://www.gfxtra31.com/user/dimsons/news/rss.xml"
DEFAULT_TG_CHANNEL = "@dimsonsgfx"
DEFAULT_TG_TOKEN = "8639708447:AAGXumHk_VfSCF9W9YuYjh2rq7ImceQo_s8"

CATEGORY_MAP = [
    {
        "slug": "indesign-templates",
        "name": "InDesign Templates",
        "tag": "InDesign",
        "keywords": ["indesign", "indd", "magazine", "brochure", "editorial", "flyer", "lookbook", "annual report"]
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
        "keywords": ["mockup", "psd mockup", "packaging", "branding mockup", "scene generator", "device mockup", "iphone", "t-shirt"]
    },
    {
        "slug": "3d-print-models",
        "name": "3D Print Models",
        "tag": "3DPrint",
        "keywords": ["3d print", "stl", "obj", "3d model", "miniature", "cosplay", "action figure", "print in place"]
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
    combined = f"{title} {rss_category}".lower()
    for cat in CATEGORY_MAP:
        for kw in cat["keywords"]:
            if kw in combined:
                return cat
    # Default fallback
    if "vector" in combined or "elements" in combined:
        return CATEGORY_MAP[4]  # ui-design-kits
    return CATEGORY_MAP[0]  # fallback to indesign-templates


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
    """Extract format/size specs like 'INDD | 974 MB' or 'EPS | AI' from DLE description"""
    if not raw_html:
        return ""
    # Look for format | size patterns
    match = re.search(r'([A-Za-z0-9\s,\.]+\|[A-Za-z0-9\s,\.]+)', raw_html)
    if match:
        return match.group(1).strip()
    return ""


def download_image(img_url):
    req = urllib.request.Request(
        img_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.gfxtra31.com/"
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


def parse_rss_feed(feed_url):
    req = urllib.request.Request(
        feed_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        content = resp.read()
    root = ET.fromstring(content)
    items = []
    for item in root.findall("channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link).strip()
        category = (item.findtext("category") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        desc_html = (item.findtext("description") or "").strip()

        # Extract image URL
        img_match = re.search(r'src=["\']([^"\']+)["\']', desc_html)
        img_url = ""
        if img_match:
            img_src = img_match.group(1)
            if img_src.startswith("/"):
                img_url = "https://www.gfxtra31.com" + img_src
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


def main():
    token = os.environ.get("TG_BOT_TOKEN", DEFAULT_TG_TOKEN).strip()
    channel = os.environ.get("TG_CHANNEL", DEFAULT_TG_CHANNEL).strip()
    rss_url = os.environ.get("RSS_URL", DEFAULT_RSS_URL).strip()

    print(f"=== Starting RSS Sync ===")
    print(f"RSS Source: {rss_url}")
    print(f"Target Channel: {channel}")

    synced_items = load_synced_state()
    synced_links = {item if isinstance(item, str) else item.get("link", "") for item in synced_items}
    print(f"Previously synced items: {len(synced_links)}")

    try:
        items = parse_rss_feed(rss_url)
        print(f"Found {len(items)} items in RSS feed.")
    except Exception as e:
        print(f"Error reading RSS feed: {e}")
        return 1

    # Filter out already synced items
    new_items = [i for i in items if i["link"] not in synced_links and i["guid"] not in synced_links]
    print(f"New items to sync: {len(new_items)}")

    if not new_items:
        print("Everything is up to date!")
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
