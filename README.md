# Renoise Color Themes — Archive

A curated, attribution-preserving archive of **332 Renoise color themes (`.xrnc`)**
from two community sources:

| Source | Themes | Where |
|---|---|---|
| **Renoise Forum** — [“Color Themes For Renoise”](https://forum.renoise.com/t/color-themes-for-renoise/18003) thread, running since Sept 2006 | 229 | forum post uploads |
| **Discord** — [Renoise Themes & Stuff](https://discord.gg/hy48JMSHKc) | 103 | server attachments |

> ⚠️ **This is an archive, not an authorship claim.** Every theme is the work of its
> original author. If you are an author and want your theme removed or re-credited,
> open an issue or PR and it will be done promptly.

## What's inside

| Path | Contents |
|---|---|
| `themes/` | 332 `.xrnc` theme files. Forum files are named `<post>_<name>.xrnc` (forum post number prefix); Discord files are named `dc<message_id>_<name>.xrnc` |
| `previews/` | Rendered preview for every theme (see disclaimer below) |
| `catalog.json` | Machine-readable index: file, theme name, author/uploader, date, original filename, source URL, sha256, size |
| `dead-links.csv` | 45 external download links from the forum thread that are gone (mostly 2006–2012 hosting) — documented loss |
| `scripts/` | The harvesting scripts used to collect both archives (reproducibility) |

**Size:** ~1.6 MB of themes (~330 files) + preview images.

> ⚠️ **Preview disclaimer:** the images in `previews/` and on the
> [gallery](https://mene311.github.io/renoise-forum-color-themes/) are **not screenshots** of
> these themes running in Renoise. They are approximate renders from the renoisethemes.com
> preview engine, which recolors a reference image of the *default* Renoise UI with each theme's
> colors (unmapped pixels, text, and icons are synthesized). Always install the `.xrnc` to see
> the true look — the download is the source of truth.

## ⚠️ Attribution of Discord-sourced themes

The two sources have **different evidentiary standards**, and `catalog.json` reflects that:

- **Forum entries** carry a verified `author` — the person who posted the theme in their own thread.
- **Discord entries do NOT.** They carry `posted_by`: the account that *uploaded the file* to
  the server. That is **not** necessarily the author. The server's featured (`★`) channels are
  moderator-curated showcases and demonstrably contain **re-posts of third-party themes** — e.g.
  the same file uploaded there by one account is published on the forum by a different author
  (Colorful beauty → NPC1, Ableton Live 10 → grymmjack, 808Dark → floodmyth,
  eDEX-UI interstellar → imapeppertoo).

Of the 103 Discord themes, **101 were uploaded from curated `★` channels**, so authorship was
left `null` rather than guessed. De-duplication *by sha256* against the forum archive caught
6 files that were already present under their true attribution — those were skipped rather
than added twice.

If you authored one of these and want credit, open an issue with the theme name.

## Why only 229 from the forum?

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
# Forum source
python3 scripts/names_pass.py    # enumerate + name pass (requires the thread JSON API)
python3 scripts/harvest.py       # download (polite, ~1 req/s)
python3 scripts/harvest_discord.py  # Discord source (requires a logged-in Discord session)

# catalog.json = harvest manifest, reformatted
```

`harvest_discord.py` reads the Discord API token and Cloudflare cookies from a local Firefox
profile, and requires membership of the server. It dedupes by sha256 **both** internally and
against the existing `catalog.json`.

Previews are rendered with the renoisethemes.com preview engine:

```js
import { parseThemeFile } from './lib/parser.js';
import { generatePreviews } from './lib/preview-renderer.js';
const { elementColorMap } = parseThemeFile('themes/<file>.xrnc');
const res = await generatePreviews(elementColorMap, outDir); // → { pattern, mixer, waveform }
```

## Provenance & licensing

- Theme files © their respective authors (see `catalog.json` for attribution)
- Repo metadata, README, and scripts: [CC0-1.0](LICENSE)

### Source notes

- Discord attachment URLs contain **expiring** signed parameters (`ex`/`is`/`hm`). `catalog.json`
  stores the canonical path with the signature stripped; the file committed in `themes/` is the
  durable copy. Discord has previously announced (and shelved) plans to expire attachments after
  24h — if that ever lands, this archive is the backup.
- Discord uploads were captured 2026-09-10; the server's most recent theme activity was 2026-07-31.
