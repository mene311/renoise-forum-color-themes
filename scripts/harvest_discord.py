#!/usr/bin/env python3
"""Harvest Renoise .xrnc colour themes from the "Renoise Themes & Stuff" Discord server.

Auth reuses a local, logged-in Discord web session (no OAuth app, no bot):
  * API token  -> plaintext in localStorage:  storage/default/https+++discord.com/ls/data.sqlite
  * CF cookies -> cookies.sqlite  (cf_clearance, __cf_bm, __dcfduid, __sdcfduid)
Both live inside the Firefox profile. Read in immutable mode so a running Firefox is fine.

Requires membership of the guild. Read-only: never POSTs.

Usage:
  python3 harvest_discord.py --out ../discord-dl --write-catalog

Then dedupe/skip is by sha256 against ../catalog.json (so already-archived themes are skipped).
"""
import argparse, datetime, hashlib, json, os, re, sqlite3, sys, time
import urllib.request, urllib.error

GUILD = '886096835477917766'          # Renoise Themes & Stuff
INVITE = 'https://discord.gg/hy48JMSHKc'
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0'
PROFILE = os.path.expanduser('~/.mozilla/firefox/qqjz1cid.default-release')
TOKEN_DB = PROFILE + '/storage/default/https+++discord.com/ls/data.sqlite'
COOKIE_DB = PROFILE + '/cookies.sqlite'
URL_RE = re.compile(r'/attachments/(\d+)/(\d+)/')


def get_token():
    con = sqlite3.connect(f'file:{TOKEN_DB}?immutable=1', uri=True)
    return con.execute("select value from data where key='token'").fetchone()[0] \
              .decode().strip().strip('"')


def get_cookies():
    con = sqlite3.connect(f'file:{COOKIE_DB}?immutable=1', uri=True)
    return {n: v for _, n, v in con.execute(
        "select host,name,value from moz_cookies where host like '%discord%' "
        "and name in ('cf_clearance','__cf_bm','__dcfduid','__sdcfduid')").fetchall()}


TOKEN, COOKIES = get_token(), get_cookies()


def api(path):
    req = urllib.request.Request('https://discord.com/api/v9' + path,
                                 headers={'Authorization': TOKEN, 'User-Agent': UA,
                                          'Accept': 'application/json'})
    if COOKIES:
        req.add_header('Cookie', '; '.join(f'{k}={v}' for k, v in COOKIES.items()))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(2 + attempt * 3); continue
            return e.code, None
        except Exception:
            time.sleep(2)
    return -1, None


def iso(mid):
    return datetime.datetime.fromtimestamp(
        ((int(mid) >> 22) + 1420070400000) / 1000, datetime.UTC).isoformat(timespec='minutes')


def safe(name):
    return re.sub(r'[^\w\s.\-()]+', '_', name).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='./discord-dl')
    ap.add_argument('--catalog', default='./catalog.json',
                    help='existing catalog.json, used for sha256 dedupe')
    ap.add_argument('--write-catalog', action='store_true')
    a = ap.parse_args()

    known = set()
    if os.path.exists(a.catalog):
        for t in json.load(open(a.catalog)).get('themes', []):
            if t.get('sha256'):
                known.add(t['sha256'])
        print(f'[i] {len(known)} themes already catalogued (sha256 dedupe)', file=sys.stderr)

    st, chans = api(f'/guilds/{GUILD}/channels')
    if st != 200:
        sys.exit(f'cannot list channels (http {st}) — token stale or not a member?')
    text = [c for c in chans if c['type'] == 0]
    print(f'[i] {len(text)} text channels', file=sys.stderr)

    os.makedirs(a.out, exist_ok=True)
    entries, seen, skipped = [], set(), 0

    for i, ch in enumerate(text):
        st, msgs = api(f"/channels/{ch['id']}/messages?limit=100")
        if st != 200:
            print(f'  [{i+1}/{len(text)}] #{ch["name"]}: http {st} (skipped)', file=sys.stderr)
            time.sleep(0.5); continue
        for m in msgs:
            for att in m.get('attachments', []):
                if not att['filename'].lower().endswith('.xrnc'):
                    continue
                mm = URL_RE.search(att['url'])
                ch_id, msg_id = (mm.group(1), mm.group(2)) if mm else ('', '')
                try:
                    r = urllib.request.Request(att['url'], headers={'User-Agent': UA})
                    with urllib.request.urlopen(r, timeout=40) as resp:
                        blob = resp.read()
                except Exception as e:
                    print(f'  ! download failed {att["filename"]}: {e}', file=sys.stderr); continue
                sha = hashlib.sha256(blob).hexdigest()
                if sha in seen or sha in known:
                    skipped += 1; continue
                seen.add(sha)
                fname = safe(f'dc{msg_id}_{att["filename"]}')
                open(os.path.join(a.out, fname), 'wb').write(blob)
                stem = fname[:-5]
                entries.append({
                    'file': fname,
                    'name': stem.split('_', 1)[1].replace('_', ' ').strip() if '_' in stem else stem,
                    'author': None,                      # NOT inferable — see README
                    'posted_by': m['author'].get('username') or '?',
                    'posted_in': f'#{ch["name"]}',
                    'channel_id': ch_id, 'message_id': msg_id,
                    'date': iso(m['id'])[:10],
                    'original_filename': att['filename'],
                    'url': att['url'].split('?')[0],     # strip expiring signature
                    'sha256': sha, 'size_bytes': len(blob), 'source': 'discord',
                })
                time.sleep(0.25)
        print(f'  [{i+1}/{len(text)}] #{ch["name"]}: {len(entries)} kept', file=sys.stderr)
        time.sleep(0.45)

    entries.sort(key=lambda e: (e['date'], e['name']))
    json.dump(entries, open(os.path.join(a.out, 'manifest.json'), 'w'), indent=1,
              ensure_ascii=False)
    print(f'\n{len(entries)} unique new themes -> {a.out}  ({skipped} duplicates skipped)')

    if a.write_catalog:
        cat = json.load(open(a.catalog))
        cat['themes'].extend(entries)
        cat.setdefault('counts', {})['discord'] = len(entries)
        cat['count'] = len(cat['themes'])
        json.dump(cat, open(a.catalog, 'w'), indent=1, ensure_ascii=False)
        print(f'catalog.json updated -> {cat["count"]} themes')


if __name__ == '__main__':
    main()
