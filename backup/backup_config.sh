#!/bin/bash

# Set variables
CONFIG_STORAGE="/home/shady/Documents/tmp/config"
BACKUP_REPO="/home/shady/Documents/tmp/backups"
PASSWORD_FILE="/data/resticPassword.txt"

# Check if the password file exists
if [[ ! -f "$PASSWORD_FILE" ]]; then
    echo "Password file not found: $PASSWORD_FILE"
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
        restic backup --repo "$restic_repo" "$folder" --compression max

        # Prune old backups
        echo "Pruning old backups for $restic_repo..."
        restic forget --repo "$restic_repo" --keep-yearly 2 --keep-monthly 12 --keep-weekly 4 --keep-daily 7 --prune
    fi
done

echo "Backup completed"
