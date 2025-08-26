#!/bin/bash

# Set variables
CONFIG_STORAGE="/home/shady/Documents/tmp/config"
BACKUP_REPO="/home/shady/Documents/tmp/backups"
PASSWORD_FILE="/data/resticPassword.txt"
NTFY_URL="https://ntfy.holmlab.org/backupsqY5CmNgp0cHv9UjeEzrnTT8qORA5M1qWUn"

# Check if the password file exists
if [[ ! -f "$PASSWORD_FILE" ]]; then
    echo "Password file not found: $PASSWORD_FILE"
    curl -X POST "$NTFY_URL" -d "🔒 Error: Password file not found: $PASSWORD_FILE" -H "Priority: high"
    exit 1
fi

# Export the Restic password file
export RESTIC_PASSWORD_FILE="$PASSWORD_FILE"

# Initialize variables for summary
success_count=0
error_count=0
backup_details=""
folder_sizes=""

# Loop through each folder in the config_storage directory
for folder in "$CONFIG_STORAGE"/*; do
    if [[ -d "$folder" ]]; then
        # Get the folder name
        folder_name=$(basename "$folder")
        
        # Calculate the folder size
        folder_size=$(du -sh "$folder" | cut -f1)
        folder_sizes+="$folder_name: $folder_size\n"

        # Set the Restic repository path
        restic_repo="$BACKUP_REPO/$folder_name"

        # Initialize the Restic repository if it doesn't exist
        if ! restic init --repo "$restic_repo" 2>/dev/null; then
            echo "Restic repository already exists: $restic_repo"
        fi

        # Perform the backup and capture output
        echo "Backing up $folder to $restic_repo..."
        backup_output=$(restic backup --repo "$restic_repo" "$folder" --compression max 2>&1)
        if [[ $? -eq 0 ]]; then
            success_count=$((success_count + 1))
            backup_details+="Backup successful for: $folder_name\n"
        else
            error_count=$((error_count + 1))
            backup_details+="Error during backup for: $folder_name\n"
        fi

        # Prune old backups and capture output
        echo "Pruning old backups for $restic_repo..."
        prune_output=$(restic forget --repo "$restic_repo" --keep-yearly 2 --keep-monthly 12 --keep-weekly 4 --keep-daily 7 --prune 2>&1)
        if [[ $? -eq 0 ]]; then
            success_count=$((success_count + 1))
            backup_details+="Pruning successful for: $folder_name\n"
        else
            error_count=$((error_count + 1))
            backup_details+="Error during pruning for: $folder_name\n"
        fi
    fi
done

# Sort folder sizes from large to small
sorted_folder_sizes=$(echo -e "$folder_sizes" | sort -hr -k2)

# Prepare the notification message
if [[ $error_count -eq 0 ]]; then
    message="✅ All backups and pruning completed successfully!\nFolder sizes:\n$sorted_folder_sizes\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n$backup_details"
    priority="min"
else
    message="❌ Backup and pruning completed with errors!\nFolder sizes:\n$sorted_folder_sizes\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n$backup_details"
    priority="high"
fi

# Use printf to format the message correctly
formatted_message=$(printf "%b" "$message")

# Send a summarizing notification as JSON with priority
curl -H "Priority: "$priority"" -X POST "$NTFY_URL" -H "Content-Type: application/json" -d "$formatted_message"

echo "Backup and pruning completed."
