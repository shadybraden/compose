#!/bin/bash

# variables:
PASSWORD_FILE="/data/resticPassword.txt"

DATA_STORAGE="/data/config_storage"
BACKUP_REPO="/data/backups"
NTFY_URL="https://ntfy.holmlab.org/backupsqY5CmNgp0cHv9UjeEzrnTT8qORA5M1qWUn"
ERROR_LOG="/data/restic_error_log.txt"
success_count=0
error_count=0
backup_details=""
folder_sizes=""
total_original_size=0
total_backup_size=0

# make sure the password file exists
if [[ ! -f "$PASSWORD_FILE" ]]; then
    echo "Password file not found: $PASSWORD_FILE" | tee -a "$ERROR_LOG"
    curl -X POST "$NTFY_URL" -d "🔒 Error: Password file not found: $PASSWORD_FILE" -H "Priority: high"
    exit 1
fi

# Export the Restic password file
export RESTIC_PASSWORD_FILE="$PASSWORD_FILE"

# Loop through each folder in the $DATA_STORAGE directory
for folder in "$DATA_STORAGE"/*; do
    if [[ -d "$folder" ]]; then
        # Get the folder name
        folder_name=$(basename "$folder")
        
        # Calculate the original folder size
        original_size=$(du -sb "$folder" | cut -f1)
        total_original_size=$((total_original_size + original_size))

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
            echo "Error during backup for: $folder_name\n$backup_output" | tee -a "$ERROR_LOG"
            backup_details+="Error during backup for: $folder_name\n"
        fi

        # Calculate the backup folder size
        backup_size=$(du -sb "$restic_repo" | cut -f1)
        total_backup_size=$((total_backup_size + backup_size))

        # Add folder size comparison to the report
        folder_sizes+="$folder_name: $(numfmt --to=iec-i --from=auto "$original_size") --> $(numfmt --to=iec-i --from=auto "$backup_size")\n"

        # Prune old backups and capture output
        echo "Pruning old backups for $restic_repo..."
        prune_output=$(restic forget --repo "$restic_repo" --keep-yearly 2 --keep-monthly 12 --keep-weekly 4 --keep-daily 7 --prune 2>&1)
        if [[ $? -eq 0 ]]; then
            success_count=$((success_count + 1))
            backup_details+="Pruning successful for: $folder_name\n"
        else
            error_count=$((error_count + 1))
            echo "Error during pruning for: $folder_name\n$prune_output" | tee -a "$ERROR_LOG"
            backup_details+="Error during pruning for: $folder_name\n"
        fi
    fi
done

# Sort folder sizes from large to small
sorted_folder_sizes=$(echo -e "$folder_sizes" | sort -hr -k2)

# Prepare the total sizes in human-readable format
total_original_human=$(numfmt --to=iec-i --from=auto "$total_original_size")
total_backup_human=$(numfmt --to=iec-i --from=auto "$total_backup_size")

# Prepare the notification message
if [[ $error_count -eq 0 ]]; then
    message="✅-$(hostname)!\nVols: ($total_original_human --> $total_backup_human)\n$sorted_folder_sizes"
    priority="min"
else
    message="❌ Backup and pruning completed with errors!\nFolder sizes: ($total_original_human --> $total_backup_human)\n$sorted_folder_sizes\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n$backup_details"
    priority="high"
fi

# Use printf to format the message correctly
formatted_message=$(printf "%b" "$message")

# Send a summarizing notification as JSON with priority
curl -H "Tags: envelope_with_arrow" -H "Priority: $priority" -X POST "$NTFY_URL" -H "Content-Type: application/json" -d "$formatted_message"

echo "Backup and pruning completed."
