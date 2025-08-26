#!/bin/bash

# Set variables
CONFIG_STORAGE="/home/shady/Documents/tmp/config"
BACKUP_REPO="/home/shady/Documents/tmp/backups"
PASSWORD_FILE="/data/resticPassword.txt"
NTFY_URL="https://ntfy.holmlab.org/backupsqY5CmNgp0cHv9UjeEzrnTT8qORA5M1qWUn"

# Check if the password file exists
if [[ ! -f "$PASSWORD_FILE" ]]; then
    echo "Password file not found: $PASSWORD_FILE"
    curl -X POST "$NTFY_URL" -d "🔒 Error: Password file not found: $PASSWORD_FILE"
    exit 1
fi

# Export the Restic password file
export RESTIC_PASSWORD_FILE="$PASSWORD_FILE"

# Loop through each folder in the config_storage directory
for folder in "$CONFIG_STORAGE"/*; do
    if [[ -d "$folder" ]]; then
        # Get the folder name
        folder_name=$(basename "$folder")
        
        # Set the Restic repository path
        restic_repo="$BACKUP_REPO/$folder_name"

        # Initialize the Restic repository if it doesn't exist
        if ! restic init --repo "$restic_repo" 2>/dev/null; then
            echo "Restic repository already exists: $restic_repo"
        fi

        # Perform the backup
        echo "Backing up $folder to $restic_repo..."
        if restic backup --repo "$restic_repo" "$folder" --compression max; then
            curl -X POST "$NTFY_URL" -d "✅ Backup successful for: $folder_name"
        else
            curl -X POST "$NTFY_URL" -d "❌ Error during backup for: $folder_name"
        fi

        # Prune old backups
        echo "Pruning old backups for $restic_repo..."
        if restic forget --repo "$restic_repo" --keep-yearly 2 --keep-monthly 12 --keep-weekly 4 --keep-daily 7 --prune; then
            curl -X POST "$NTFY_URL" -d "🧹 Pruning successful for: $folder_name"
        else
            curl -X POST "$NTFY_URL" -d "❌ Error during pruning for: $folder_name"
        fi
    fi
done

echo "Backup and pruning completed."
