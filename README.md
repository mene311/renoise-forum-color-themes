# Renoise Color Themes — Archive

A curated, attribution-preserving archive of **561 Renoise color themes (`.xrnc`)**
from four community sources:

| Source | Themes | Where |
|---|---|---|
| **Renoise Forum** — [“Color Themes For Renoise”](https://forum.renoise.com/t/color-themes-for-renoise/18003) thread, running since Sept 2006 | 229 | forum post uploads |
| **Official Renoise theme gallery** (webftp mirror, captured 2022-03) | 95 | `<Author>-<Theme>` folders — **author verified from the gallery itself** |
| **Discord** — [Renoise Themes & Stuff](https://discord.gg/hy48JMSHKc) | 103 | server attachments, mostly mod-curated `★` showcase channels |
| **Discord** — Renoise Community Server (`#themes`, incl. a 128-file `themes.zip`) | 145 → 134 after de-duplication | server attachments |

**324 of 561 themes carry a verified author** (forum 229 + gallery 95). The other 237 are Discord uploads where authorship could not be proven — see below.

> ⚠️ **This is an archive, not an authorship claim.** Every theme is the work of its
> original author. If you are an author and want your theme removed or re-credited,
> open an issue or PR and it will be done promptly.

## What's inside

| Path | Contents |
|---|---|
| `themes/` | 561 `.xrnc` theme files. Naming: forum `<post>_<name>.xrnc` · official gallery `webftp_<name>.xrnc` · Discord `dc<message_id>_<name>.xrnc` · bulk zip `zth_<name>.xrnc` |
| `previews/` | Rendered preview for every theme (see disclaimer below) |
| `catalog.json` | Machine-readable index: file, theme name, author/uploader, date, original filename, source URL, sha256, size |
| `dead-links.csv` | 45 external download links from the forum thread that are gone (mostly 2006–2012 hosting) — documented loss |
| `scripts/` | The harvesting scripts used to collect both archives (reproducibility) |

**Size:** ~2.9 MB of themes (561 files) + preview images.

> ⚠️ **Preview disclaimer:** the images in `previews/` and on the
> [gallery](https://mene311.github.io/renoise-forum-color-themes/) are **not screenshots** of
> these themes running in Renoise. They are approximate renders from the renoisethemes.com
> preview engine, which recolors a reference image of the *default* Renoise UI with each theme's
> colors (unmapped pixels, text, and icons are synthesized). Always install the `.xrnc` to see
> the true look — the download is the source of truth.

## De-duplication

Same-named files were **not** assumed to be duplicates — many are deliberate version series by one
author. So every theme was fingerprinted by its **actual colour map** (parsed from the `.xrnc` XML),
and two files count as identical only if all ~86 colour elements match.

**11 entries were collapsed** (572 → 561) and preserved in `catalog.json` under `aliases`, so the
upload record survives even though the redundant file is gone:

| Kind | Example | Why collapsed |
|---|---|---|
| Identical colour map | `Amiga_OS_Theme_Final_other{,_2,_3,_4}` — 4 files, byte-different, *colour-identical* | Genuinely the same theme |
| Same theme on two sites | `1160_LotuaStation - #6E58F4.xrnc` (forum) and its Discord copy; `BloodSugar (Glide)` likewise | Same author re-uploaded to a second site; only 1 of 86 elements differs (re-save noise) |

**Deliberate variants are kept**, not deleted — 6 families get a `variant_group` and the gallery shows
one card each with a `×N variants` badge (uncheck *group variants* to see every file):

- `Amiga_OS_Theme_Final_heller{,_1,_2,_4,_5}` — brightness variants, posted by their author as alternatives
- `Octamed8.5_buttons_other4.2.{1,2,3}` — saturation variants ("choose what you most likely")
- `solarized_plastic_RC1/RC2`, `Neon v1/v2`, `Bluey/v2`, `NoiseLabs` — explicit version series

Grouping the gallery takes it from 561 cards to **552**, with the rest one click away.

## ⚠️ Attribution of Discord-sourced themes

The sources have **different evidentiary standards**, and `catalog.json` reflects that:

- **Forum entries** carry a verified `author` — the person who posted the theme in their own thread.
- **Official-gallery entries** carry an `author` taken from the webftp gallery's `<Author>-<Theme>`
  folder names (`Achenar-City_Lights/` → Achenar) — authoritative for those 95 themes.
- **Discord entries do NOT.** They carry `posted_by`: the account that *uploaded the file*. That is
  **not** necessarily the author, and both servers are demonstrably full of re-posts:

  | Theme | Uploaded by | Actual author |
  |---|---|---|
  | Colorful beauty | corefragment | **NPC1** |
  | Ableton Live 10 (+2) | corefragment | **grymmjack** |
  | 808Dark | corefragment | **floodmyth** |
  | eDEX-UI interstellar | corefragment | **imapeppertoo** |
  | Cyberpunk1 | esaruoho | **Osionik** — uploader wrote *“this theme from Osionik looks great”* |
  | Hotdog Stand | esaruoho | **nilsding** — uploader found it on GitHub |
  | GJ-FM7 | dark_evan1 | **grymmjack** — *“FM-7 theme by Renoise forum user grymmjack”* |
  | Sononoise (×2) | noobish.wav | *unknown* — uploader: *“i dont remember where i got these”* |

  In *Renoise Themes & Stuff* the featured (`★`) channels are moderator-curated showcases, so
  `posted_by` usually is **not** the author. In *Renoise Community Server*, `#themes` carries
  requests and re-posts alongside genuine self-posts, so it's mixed either way.

Because of this, **all 237 Discord themes have `author: null`** rather than a guess —
this repo exists to preserve attribution, and mis-crediting is worse than under-crediting.
De-duplication *by sha256* across all four sources caught **18 files already present** under
their true attribution; those were skipped rather than added twice.

### The `context` field

Where the accompanying Discord message reveals the real author or lineage, it is preserved verbatim
in a `context` field on the entry — so the evidence trail survives alongside the file. Examples you
can recover from it today:

- `unblackforestcake` → *“based on Colorful (NPC1)”*
- `Ooze` → *“I made a variant on Acid Grey”*
- `Black-n-White` → *“Simple black and white theme I made.”* (uploader **is** the author here)

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
