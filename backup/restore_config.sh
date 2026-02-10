#!/bin/bash

# Check if a folder name was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <foldername>"
    exit 1
fi

# Set variables
FOLDERNAME=$1
BACKUP_PATH="/data/backups/${FOLDERNAME}"
RESTORE_PATH="/data/${FOLDERNAME}.restore"
PASSWORD_FILE="/data/resticPassword.txt"

# Check if the backup repository exists
if [ ! -d "${BACKUP_PATH}" ]; then
    echo "Error: Backup repository for ${FOLDERNAME} does not exist in ${BACKUP_PATH}"
    exit 1
fi

# List available snapshots
echo "Available snapshots for ${FOLDERNAME}:"
RESTIC_PASSWORD_FILE="${PASSWORD_FILE}" restic -r "${BACKUP_PATH}" snapshots

# Prompt user to choose a snapshot
read -p "Enter the snapshot ID you want to restore (or press Enter for the latest): " SNAPSHOT_ID

# If no snapshot ID is provided, use the latest
if [ -z "${SNAPSHOT_ID}" ]; then
    SNAPSHOT_ID="latest"
fi

# Create restore directory if it doesn't exist
mkdir -p "${RESTORE_PATH}"

# Perform the restore
echo "Restoring snapshot ${SNAPSHOT_ID} to ${RESTORE_PATH}..."
RESTIC_PASSWORD_FILE="${PASSWORD_FILE}" restic -r "${BACKUP_PATH}" restore "${SNAPSHOT_ID}" --target "${RESTORE_PATH}"

# Check restore status
if [ $? -eq 0 ]; then
    echo "Restore completed successfully to ${RESTORE_PATH}"
else
    echo "Restore failed"
    exit 1
fi

# UNTESTED, USE AS REFERENCE:

# Copy files from RESTORE_PATH to config_storage
# cp -r "/data/${RESTORE_PATH}/data/config_storage/${FOLDERNAME}/" /data/config_storage/
