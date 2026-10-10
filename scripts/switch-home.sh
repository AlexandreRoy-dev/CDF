#!/usr/bin/env bash
# One step homepage switch. Default in this branch = new v2 homepage.
#   scripts/switch-home.sh old   -> restore the previous live index.html (from origin/main)
#   scripts/switch-home.sh new   -> back to the v2 homepage of this branch's launch commit
set -e; cd "$(dirname "$0")/.."
case "$1" in
  old) git show origin/main:index.html > index.html ;;
  new) git show lancement-secteurs-2026-10-10:index.html > index.html ;;
  *) echo "usage: $0 old|new"; exit 1 ;;
esac
echo "index.html -> $1 (commit to apply)"
