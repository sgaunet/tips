#!/bin/bash
# Notification script for security alerts

# For macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e "display notification \"$1\" with title \"Claude Code Security Alert\" subtitle \"Secrets Detected\" sound name \"Sosumi\""
fi

# For Linux with notify-send
if command -v notify-send &> /dev/null; then
    notify-send "Claude Code Security Alert" "$1" -u critical -i dialog-warning
fi

# Log to file
echo "[$(date)] Security Alert: $1" >> ~/.claude/logs/security_alerts.log