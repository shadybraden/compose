#!/usr/bin/env bash
set -euo pipefail

HOSTNAME="$(hostname)"
BACKUP_SOURCE="/data/mnt/backups"
BUCKET_NAME="resticlydjakqyscraednslu"
NTFY_URL="https://ntfy.holmlab.org/backupsqY5CmNgp0cHv9UjeEzrnTT8qORA5M1qWUn"

log() {
    printf '[%s] %s\n' "$(date +'%Y-%m-%d %H:%M:%S')" "$*"
}

command -v rclone >/dev/null 2>&1 || { log "Error: rclone is not installed. Please install rclone first."; exit 1; }

if [ ! -d "$BACKUP_SOURCE" ]; then
    log "Error: Backup source directory '$BACKUP_SOURCE' does not exist."
    exit 1
fi

START_TIME=$(date +%s)
TOTAL_SIZE=0
ANY_SYNCED=0

shopt -s nullglob
for backup_dir in "$BACKUP_SOURCE"/*/; do
    [ -d "$backup_dir" ] || continue
    BACKUP_NAME="$(basename "${backup_dir%/}")"
    S3_DESTINATION="aws://${BUCKET_NAME}/${HOSTNAME}/${BACKUP_NAME}"

    log "Syncing '$backup_dir' -> '$S3_DESTINATION'"

    if rclone sync "$backup_dir" "$S3_DESTINATION" \
        --s3-storage-class DEEP_ARCHIVE \
        --verbose \
        --transfers 4 \
        --checkers 8 \
        --contimeout 60s \
        --timeout 300s \
        --retries 3 \
        --low-level-retries 10
    then
        log "Successfully synced '$BACKUP_NAME' to S3"
        # use du -sb when available, otherwise fall back to du -sk
        if dir_size_bytes=$(du -sb "$backup_dir" 2>/dev/null | cut -f1); then
            :
        else
            # fallback to kilobytes then convert
            dir_kb=$(du -sk "$backup_dir" | cut -f1)
            dir_size_bytes=$((dir_kb * 1024))
        fi
        TOTAL_SIZE=$((TOTAL_SIZE + dir_size_bytes))
        ANY_SYNCED=1
    else
        log "Error: Failed to sync '$BACKUP_NAME' to S3"
    fi
done
shopt -u nullglob

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_HOURS=$((DURATION / 3600))
DURATION_MINUTES=$(((DURATION % 3600) / 60))
DURATION_SECONDS=$((DURATION % 60))

# Human readable size: prefer numfmt if available
if command -v numfmt >/dev/null 2>&1; then
    HR_SIZE="$(numfmt --to=iec-i --suffix=B "$TOTAL_SIZE" 2>/dev/null || echo "${TOTAL_SIZE}B")"
else
    HR_SIZE="${TOTAL_SIZE}B"
fi

NTFY_PAYLOAD="Total data in S3: ${HR_SIZE}
Duration: ${DURATION_HOURS}h ${DURATION_MINUTES}m ${DURATION_SECONDS}s"

# send notification
if command -v curl >/dev/null 2>&1; then
    curl -sS -X POST "$NTFY_URL" \
        -H "Tags: outbox_tray" \
        -H "Title: ${HOSTNAME} backups uploaded!" \
        -H "Priority: min" \
        --data-binary "$NTFY_PAYLOAD" || log "Warning: failed to send ntfy notification"
else
    log "Warning: curl not available; skipping ntfy notification"
fi

log "Backup sync process completed (any synced: $ANY_SYNCED, total_bytes: $TOTAL_SIZE)"
