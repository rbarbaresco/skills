#!/usr/bin/env bash
# Undo one /stations run by replaying its MANIFEST.tsv bottom-up.
#
# MANIFEST.tsv: a header line, then one tab-separated row per action, in the order applied:
#   move    <old path>  <new path>     undo: move it back
#   edit    <path>      <backup copy>  undo: copy the pre-edit file back over it
#   create  -           <path>         undo: move it into ./undone/ (files, links, folders)
#
# Nothing is deleted: whatever the run created ends up in ./undone/, logins included.
set -euo pipefail
cd "$(dirname "$0")"

tail -n +2 MANIFEST.tsv | awk '{ rows[NR] = $0 } END { for (i = NR; i > 0; i--) print rows[i] }' |
while IFS=$'\t' read -r action from to; do
  case $action in
    move)   mkdir -p "$(dirname "$from")" && mv "$to" "$from" ;;
    edit)   cp -a "$to" "$from" ;;
    create) mkdir -p "undone$(dirname "$to")" && mv "$to" "undone$to" ;;
    *)      echo "unknown action '$action', stopping" >&2; exit 1 ;;
  esac
  echo "undone: $action $from -> $to"
done
