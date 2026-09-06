# Renoise Forum Color Themes — Archive

A curated, attribution-preserving archive of **229 Renoise color themes (`.xrnc`)**
collected from the Renoise community forum thread
**[“Color Themes For Renoise”](https://forum.renoise.com/t/color-themes-for-renoise/18003)** —
running since September 2006 and still active.

> ⚠️ **This is an archive, not an authorship claim.** Every theme is the work of its
> original author (credited in `catalog.json`). If you are an author and want your
> theme removed or re-credited, open an issue or PR and it will be done promptly.

## What's inside

| Path | Contents |
|---|---|
| `themes/` | 229 `.xrnc` theme files, named `<post>_<name>.xrnc` (forum post number prefix) |
| `catalog.json` | Machine-readable index: file, theme name, author, forum post #, date, original filename, source URL, sha256, size |
| `dead-links.csv` | 45 external download links from the thread that are gone (mostly 2006–2012 hosting) — documented loss |
| `scripts/` | The harvesting scripts used to collect the archive (reproducibility) |

**Size:** ~1.1 MB of themes. Tiny, no Git LFS needed.

## Why only 229?

The thread spans 2006 → present with 1,161 posts. Themes posted before ~2019 lived on
external hosts (rapidshare, megaupload, personal sites…) whose links have since rotted,
mostly without Wayback Machine snapshots. What survives and is archived here:

- **229 forum-hosted uploads** (2019–present + a few earlier re-posts) — the stable, canonical set
- ~16 additional external-hosted files still live at their original URLs — **not included**
  here (they're reachable at source and would duplicate provenance); see the thread
- 45 dead links are catalogued in `dead-links.csv` for future recovery attempts

## Install a theme in Renoise

1. Download any `.xrnc` from `themes/`
2. In Renoise: `Edit ▸ Preferences ▸ Appearance ▸ Themes ▸ Install/Import…` (or drop the file into `~/.config/Renoise/V3.5.4/Themes/`)
3. Select it from the theme dropdown

## Reproducing the archive

```bash
# 1. Enumerate + name pass  (requires the thread JSON API)
python3 scripts/names_pass.py
# 2. Download (polite, ~1 req/s)
python3 scripts/harvest.py
# 3. catalog.json = harvest manifest, reformatted
```

## Provenance & licensing

- Theme files © their respective authors (see `catalog.json` for attribution)
- Repo metadata, README, and scripts: [CC0-1.0](LICENSE)
- Source thread: <https://forum.renoise.com/t/color-themes-for-renoise/18003>
- Harvest date: 2026-09-06 · crawler fetched only public Discourse JSON, no account, no API key

## Related

- Interactive browsing/previews (pattern-view renders of every theme): **renoisethemes.com**
- Renoise itself: <https://www.renoise.com>
