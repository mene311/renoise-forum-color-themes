#!/usr/bin/env python3
"""Phase D1: map forum .xrnc URLs -> real filename (anchor text) + full post text.

Fetches all thread pages once; captures for EVERY post its cleaned text (for
descriptions) and for every forum-hosted .xrnc link the anchor text (the real
filename Discourse shows). Outputs notes/forum-tools/names.json:

  { "urls": { "<url>": {"anchor": "...", "post": N, "author": "...", "date": "..."} },
    "posts": { "N": "cleaned post text (~1500 chars)" } }
"""
import json, re, time, html, urllib.request

BASE = "/home/meneses/Projects/renoise/themes/notes"
TOPIC = "https://forum.renoise.com/t/color-themes-for-renoise/18003.json"
UA = {"User-Agent": "Mozilla/5.0 (archive harvest research)"}
OUT = f"{BASE}/forum-tools/names.json"
META = json.load(open(f"{BASE}/forum-18003-catalog.json"))
highest = META.get('highest_post_number', 1202)
pages = (highest + 19) // 20

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def clean_text(cooked, limit=1500):
    cooked = re.sub(r'<aside[^>]*>.*?</aside>', ' ', cooked, flags=re.S)  # drop quotes
    txt = re.sub(r'<[^>]+>', ' ', cooked)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt[:limit]

urls, posts = {}, {}
for pg in range(1, pages + 1):
    d = fetch(f"{TOPIC}?page={pg}")
    for p in d['post_stream']['posts']:
        pn = p['post_number']
        user = p.get('username', '')
        date = p.get('created_at', '')[:10]
        cooked = p.get('cooked', '')
        posts[pn] = clean_text(cooked)
        for m in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', cooked, flags=re.S):
            url, inner = m.group(1), m.group(2)
            if 'uploads/short-url/' in url and url.rstrip('/').lower().endswith('.xrnc'):
                anchor = re.sub(r'<[^>]+>', '', inner)
                anchor = html.unescape(anchor).strip()
                # keep first (usually most descriptive) anchor per url
                if url not in urls:
                    urls[url] = {'anchor': anchor, 'post': pn, 'author': user, 'date': date}
    if pg % 20 == 0:
        print(f"page {pg}/{pages} urls={len(urls)}", flush=True)
    time.sleep(0.4)

json.dump({'urls': urls, 'posts': posts}, open(OUT, 'w'), indent=1)
print(f"saved {len(urls)} url mappings + {len(posts)} post texts -> {OUT}")
