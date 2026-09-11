#!/usr/bin/env bash
# install.sh — make this archive visible to Renoise.
#
#   ./install.sh              link every theme into Renoise's Themes folder
#   ./install.sh --check      report status only, change nothing
#   ./install.sh --uninstall  remove this archive's themes from Renoise
#   ./install.sh --copy       copy instead of hardlink (separate filesystem)
#
# Renoise reads its theme library from ~/.config/Renoise/<VERSION>/Themes/ and that
# path is version-scoped, so themes do NOT follow a Renoise upgrade. Re-run this
# script after upgrading (it auto-detects the newest V* folder).
#
# On the same filesystem themes are HARDLINKED: one file, two names, no drift, and
# no risk of Renoise ignoring them the way it might ignore symlinks.
# `git pull`/`checkout` replace files and break hardlinks — re-run after those.
#
# NOTE: Renoise splits its theme picker into the main list and a "More" tab for
# older-format themes (doc_version below the newest). Both are installed; the
# summary at the end says how they split.
set -euo pipefail

cd "$(dirname "$0")"
MODE="${1:-link}"
CONFIG_ROOT="${RENOISE_CONFIG:-$HOME/.config/Renoise}"

# themes live in ./themes/ in this repo; fall back to the repo root if ever moved
SRC_DIR="themes"
[[ -d "$SRC_DIR" ]] || SRC_DIR="."
SRC=$(find "$SRC_DIR" -maxdepth 1 -name '*.xrnc' | wc -l)
if [[ "$SRC" -eq 0 ]]; then
  echo "!! found 0 .xrnc files under $SRC_DIR — refusing to report success" >&2
  exit 1
fi

THEMES_DIR=""
while IFS= read -r d; do THEMES_DIR="$d"; break; done < <(
  find "$CONFIG_ROOT" -maxdepth 2 -type d -name Themes 2>/dev/null | sort -V -r
)
if [[ -z "$THEMES_DIR" ]]; then
  echo "!! no Renoise Themes folder under $CONFIG_ROOT (expected e.g. $CONFIG_ROOT/V3.5.4/Themes)" >&2
  exit 1
fi
echo "source: $SRC_DIR ($SRC themes)"
echo "target: $THEMES_DIR"

same_fs() { [[ "$(stat -c %d "$1")" == "$(stat -c %d "$2")" ]]; }
USE_LINK=0
if same_fs "$SRC_DIR" "$THEMES_DIR" && [[ "$MODE" != "--copy" ]]; then USE_LINK=1; fi

shopt -s nullglob
linked=0 copied=0 current=0 fixed=0 missing=0 removed=0 kept=0

if [[ "$MODE" == "--uninstall" ]]; then
  for src in "$SRC_DIR"/*.xrnc; do
    dst="$THEMES_DIR/$(basename "$src")"
    [[ -e "$dst" ]] || continue
    if cmp -s "$src" "$dst"; then rm -f "$dst"; removed=$((removed+1))
    else echo "  kept (differs from repo, not ours to remove): $(basename "$src")"; kept=$((kept+1)); fi
  done
  echo; echo "removed $removed theme(s); kept $kept."
  exit 0
fi

for src in "$SRC_DIR"/*.xrnc; do
  base=$(basename "$src")
  dst="$THEMES_DIR/$base"

  if [[ ! -e "$dst" ]]; then
    if [[ "$MODE" == "--check" ]]; then printf '  NOT INSTALLED  %s\n' "$base"; missing=$((missing+1)); continue; fi
    if [[ "$USE_LINK" -eq 1 ]]; then ln "$src" "$dst"; linked=$((linked+1)); else cp -p "$src" "$dst"; copied=$((copied+1)); fi
    continue
  fi

  if cmp -s "$src" "$dst"; then
    if [[ "$(stat -c %i "$src")" == "$(stat -c %i "$dst")" ]] || [[ "$MODE" == "--check" ]] || [[ "$USE_LINK" -eq 0 ]]; then
      current=$((current+1))
    else
      ln -f "$src" "$dst"; fixed=$((fixed+1))
    fi
  else
    printf '  DIFFERS  %s (repo %s B vs installed %s B)\n' "$base" "$(stat -c %s "$src")" "$(stat -c %s "$dst")"
    if [[ "$MODE" != "--check" ]]; then
      if [[ "$USE_LINK" -eq 1 ]]; then ln -f "$src" "$dst"; else cp -p "$src" "$dst"; fi
      fixed=$((fixed+1))
    fi
  fi
done

echo
printf 'in sync: %d | linked: %d | copied: %d | fixed: %d | not installed: %d\n' \
  "$current" "$linked" "$copied" "$fixed" "$missing"

if [[ "$MODE" == "--check" ]]; then
  if [[ "$missing" -eq 0 && "$fixed" -eq 0 ]]; then echo "OK: all $SRC archive themes are visible to Renoise."
  else echo "Not fully installed: $missing missing, $fixed would be fixed — run ./install.sh"; fi
  exit 0
fi

# how they'll appear in Renoise's picker
newest=0
for src in "$SRC_DIR"/*.xrnc; do
  v=$(sed -n 's/.*doc_version="\([0-9]*\)".*/\1/p' "$src" | head -1)
  [[ -n "$v" && "$v" -gt "$newest" ]] && newest="$v"
done
modern=0; old=0
for src in "$SRC_DIR"/*.xrnc; do
  v=$(sed -n 's/.*doc_version="\([0-9]*\)".*/\1/p' "$src" | head -1)
  [[ -z "$v" ]] && continue
  if [[ "$v" -eq "$newest" ]]; then modern=$((modern+1)); else old=$((old+1)); fi
done
echo
echo "Renoise: Preferences > Appearance > Themes"
echo "  main list (doc_version $newest) : ~$modern themes"
echo "  \"More\" tab (older formats)    : ~$old themes"
echo
echo "installed total in $THEMES_DIR: $(find "$THEMES_DIR" -maxdepth 1 -name '*.xrnc' | wc -l)"
