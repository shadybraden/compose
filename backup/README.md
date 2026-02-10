# Backups

Set permissions via: https://git.holmlab.org/shady/IaC/src/branch/main/restic_perms.yaml

## backup_config.sh

`sudo su`
`crontab -e`

`0 */6 * * * /data/config_storage/compose/backup/backup_config.sh` (every 6 hours)

The goal here is to run backups on: `/data/config_storage`

And place them into: `/data/backups`

## backup_bulk.sh

`sudo su`
`crontab -e`

`0 3 * * * /data/config_storage/compose/backup/backup_bulk.sh` 3am

Idea here is to backup Immich. i.e. `/data/mnt/immich`

Then store these backups in the same base path; `/data/mnt/backups`

## upload.sh

`sudo su`
`crontab -e`

`0 5 * * 1 /data/config_storage/compose/backup/upload_config.sh`  (every monday at 5am)

`0 1 1 * * /data/config_storage/compose/backup/upload_bulk.sh`    (1x per month at 1am)

Send the backups to AWS

## restore.sh

Idea is to run:

`restore.sh FOLDERNAME`
