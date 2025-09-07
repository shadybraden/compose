#!/bin/bash

# * * * * * /data/config_storage/compose/factorio/factorio_bot.sh

DISCORD_WEBHOOK_URL="$(< /data/config_storage/factorio_bot.txt)"

send_discord_message() {
    local message="$1"
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\":\"$message\"}" \
         "$DISCORD_WEBHOOK_URL"
}

LOGS=$(docker logs factorio --since 1m | grep -E "JOIN|LEAVE")

if [ ! -z "$LOGS" ]; then
    while IFS= read -r log_line; do
        escaped_log=$(printf '%s' "$log_line" | sed 's/"/\\"/g')
        escaped_log=${escaped_log:27}
        
        send_discord_message "$escaped_log"
    done <<< "$LOGS"
fi
