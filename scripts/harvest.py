#!/usr/bin/env python3
"""Phase D2: download the 229 forum-hosted .xrnc theme files (polite).

Reads notes/forum-tools/names.json, downloads each unique forum .xrnc to
notes/forum-harvest/<post>_<filename>, writes manifest.json.
No re-uploading; plain file download with attribution metadata.
"""
import json, os, re, sys, time, hashlib, urllib.request, urllib.parse, random

BASE = "/home/meneses/Projects/renoise/themes/notes"
N = json.load(open(f"{BASE}/forum-tools/names.json"))
URLS = N['urls']
OUTDIR = f"{BASE}/forum-harvest"
os.makedirs(OUTDIR, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) archive preservation"}

def sanitize(name):
    name = name.strip().replace('/', '_').replace('\\', '_')
    name = re.sub(r'[\x00-\x1f<>:"|?*]', '_', name)
    return name[:140]

def choose_filename(url, anchor):
    # prefer the real forum filename (anchor) when it looks like a filename
    cand = None
    if anchor and anchor.lower().endswith('.xrnc'):
        cand = anchor
    elif anchor and '.' in anchor and not re.match(r'^(download|click|link|theme|file)$', anchor.lower()):
        cand = anchor if anchor.lower().endswith(('.xrnc', '.xml')) else anchor + '.xrnc'
    if not cand:
        cand = urllib.parse.urlparse(url).path.rsplit('/', 1)[-1]  # short-url token
    return sanitize(cand) or 'theme.xrnc'

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

manifest = []
failures = []
for i, (url, info) in enumerate(sorted(URLS.items(), key=lambda kv: kv[1]['post']), 1):
    fname = choose_filename(url, info.get('anchor', ''))
    target = os.path.join(OUTDIR, f"{info['post']:04d}_{fname}")
    n = 2
    while os.path.exists(target):
        base, ext = os.path.splitext(target)
        target = f"{base}-{n}{ext}"; n += 1
    abs_url = url if url.startswith('http') else 'https://forum.renoise.com' + url
    ok = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(abs_url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
                final = r.geturl()
            if len(data) == 0:
                raise ValueError('empty body')
            with open(target, 'wb') as f:
                f.write(data)
            ok = True
            manifest.append({
                'url': abs_url, 'final_url': final, 'file': os.path.basename(target),
                'post': info['post'], 'author': info['author'], 'date': info['date'],
                'anchor': info.get('anchor', ''), 'size': len(data),
                'sha256': sha(target), 'downloaded_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            })
            break
        except Exception as e:
            time.sleep(2 + attempt * 3)
    if not ok:
        failures.append({'url': abs_url, 'post': info['post'], 'author': info['author']})
    if i % 25 == 0 or not ok:
        print(f"  {i}/{len(URLS)}" + ("  FAILED: " + abs_url if not ok else ""), flush=True)
    time.sleep(0.55 + random.random() * 0.35)

json.dump({'manifest': manifest, 'failures': failures,
           'harvested_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')},
          open(f"{OUTDIR}/manifest.json", 'w'), indent=1)
total = sum(m['size'] for m in manifest)
print(f"\nharvested {len(manifest)}/{len(URLS)} files, {total/1024/1024:.1f} MB, "
      f"failures: {len(failures)}")
for f in failures:
    print("  FAIL:", f)
print(f"-> {OUTDIR}/  (+ manifest.json)")
