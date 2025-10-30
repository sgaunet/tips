
```bash
# Bash function for .bashrc
# Usage: gitcommit "2024-10-07T08:00:00" "commit message"
#        gitcommit "2 days ago" "commit message"
gitcommit() {
  local date="$1"
  local msg="$2"

  if [[ -z "$date" || -z "$msg" ]]; then
    echo "Usage: gitcommit <date> <message>" >&2
    return 1
  fi

  # Validate date using date command
  if ! date -d "$date" &>/dev/null 2>&1 && ! date -j -f "%Y-%m-%dT%H:%M:%S" "$date" &>/dev/null 2>&1; then
    echo "Error: Invalid date format '$date'" >&2
    echo "Use ISO 8601 (YYYY-MM-DDTHH:MM:SS) or relative (e.g., '2 days ago')" >&2
    return 1
  fi

  GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$msg"
}
```
