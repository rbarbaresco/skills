# stations: run `claude` with the config folder of the station you're standing in.
# Sourced from ~/.zshrc or ~/.bashrc. Edit the map below; the longest matching root wins.
# No match: the default config (~/.claude, or whatever CLAUDE_CONFIG_DIR already says).

# One station per line: <root folder>|<config folder>, for example
#   $HOME/work|$HOME/.claude-work
CLAUDE_STATIONS="
"

claude() {
  local root cfg best_root="" best_cfg=""
  while IFS='|' read -r root cfg; do
    [ -n "$root" ] || continue
    case "$PWD/" in
      "$root"/*) [ ${#root} -gt ${#best_root} ] && best_root=$root && best_cfg=$cfg ;;
    esac
  done <<< "$CLAUDE_STATIONS"

  if [ -z "$best_cfg" ]; then
    [ -t 2 ] && echo "station: default" >&2
    command claude "$@"
    return
  fi
  [ -t 2 ] && echo "station: ${best_cfg##*/.claude-}" >&2
  CLAUDE_CONFIG_DIR="$best_cfg" command claude "$@"
}
