# Backups

## backup_config.sh

The goal here is to run backups on:

/data/config_storage

And place them into:

/data/backups

## backup_bulk.sh

Idea here is to backup Immich.

i.e. /mnt/4tb/immich

Then store these backups in the same base path; /mnt/4tb/backups

## upload.sh

Send the backups to AWS

(include machine name in base folder path)
