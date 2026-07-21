#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ToolForge sprint driver (2026-07-15). Generates verified-missing pages,
regenerates sitemap.xml from disk, pings IndexNow, logs results."""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-15"
DOMAIN = "https://toolforge.io"
INDEXNOW_KEY = "9a8b7c6d"

# import template functions (trimmed copy of _sprint_gen.py)
import _tpl
_tpl.TODAY = TODAY
_tpl.DOMAIN = DOMAIN
tool_html, compare_html, blog_html = _tpl.tool_html, _tpl.compare_html, _tpl.blog_html

from _data_jul15 import TOOLS
from _data_cmpblog_jul15 import COMPARES, BLOGS

def existing(sub):
    d = os.path.join(BASE, sub)
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')} if os.path.isdir(d) else set()

tool_slugs = existing('tools')
cmp_slugs = existing('compare')
blog_slugs = existing('blog')

new_urls = []
created = {"tools": 0, "compare": 0, "blog": 0}

for t in TOOLS:
    if t['slug'] in tool_slugs:
        print("  SKIP tool", t['slug']); continue
    with open(os.path.join(BASE, 'tools', t['slug'] + '.html'), 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    created['tools'] += 1
    print("  + tools/" + t['slug'] + ".html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print("  SKIP compare", c['slug']); continue
    with open(os.path.join(BASE, 'compare', c['slug'] + '.html'), 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created['compare'] += 1
    print("  + compare/" + c['slug'] + ".html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print("  SKIP blog", b['slug']); continue
    with open(os.path.join(BASE, 'blog', b['slug'] + '.html'), 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created['blog'] += 1
    print("  + blog/" + b['slug'] + ".html")

# ---------- regenerate sitemap from disk ----------
def priority(rel):
    if rel == 'index.html' or '/' not in rel:
        return '1.0'
    if rel.startswith('category/'): return '0.6'
    if rel.startswith('tools/'): return '0.8'
    if rel.startswith('blog/'): return '0.7'
    if rel.startswith('compare/'): return '0.7'
    return '0.8'

files = []
for root, dirs, fnames in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fn in fnames:
        if fn.startswith('.') or not fn.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(root, fn), BASE).replace(os.sep, '/')
        files.append(rel)
files.sort()

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for rel in files:
    lines += ['  <url>', f'    <loc>{DOMAIN}/{rel}</loc>',
              f'    <lastmod>{TODAY}</lastmod>', '    <changefreq>weekly</changefreq>',
              f'    <priority>{priority(rel)}</priority>', '  </url>']
lines.append('</urlset>')
with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f"\nSitemap regenerated: {len(files)} URLs")

with open('/tmp/toolforge_new_urls.txt', 'w') as f:
    f.write('\n'.join(new_urls) + '\n')

# ---------- IndexNow ping ----------
def ping_indexnow(urls):
    import json, urllib.request, urllib.error
    if not urls:
        return "no new urls"
    payload = json.dumps({"host": "toolforge.io", "key": INDEXNOW_KEY, "urlList": urls}).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return f"HTTP {resp.status}: {resp.read().decode()[:200]}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    except Exception as e:
        return f"ERROR: {e}"

idx = ping_indexnow(new_urls)
print("IndexNow:", idx)

# ---------- log ----------
logpath = '/tmp/toolforge_sprint_log.md'
entry = f"\n## {TODAY} — Sprint batch (cron)\n"
entry += f"- Tools created: {created['tools']} | Compares: {created['compare']} | Blogs: {created['blog']}\n"
entry += f"- Total new URLs: {len(new_urls)}\n"
entry += f"- IndexNow: {idx}\n"
entry += "- New slugs: " + ", ".join(
    [t['slug'] for t in TOOLS if t['slug'] not in tool_slugs][:0] or
    [u.split('/')[-1] for u in new_urls]) + "\n"
with open(logpath, 'a') as f:
    f.write(entry)

print(f"\nCREATED: {created}")
print(f"TOTAL NEW URLS: {len(new_urls)}")
