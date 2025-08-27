# Backups

- [x] backup_config.sh
- [x] backup_bulk.sh
- [ ] upload.sh
- [x] restore.sh

## backup_config.sh

`sudo su && crontab -e`
`0 */6 * * * /data/config_storage/compose/backup/backup_config.sh`

The goal here is to run backups on:

/data/config_storage

And place them into:

/data/backups

## backup_bulk.sh

`sudo su && crontab -e`
`0 3 * * * /data/config_storage/compose/backup/backup_bulk.sh`

Idea here is to backup Immich.

i.e. /mnt/4tb/immich

Then store these backups in the same base path; /mnt/4tb/backups

## upload.sh

Send the backups to AWS

(include machine name in base folder path)

## restore.sh

Idea is to run:

`restore.sh FOLDERNAME`

(split into two scripts, restore_config.sh and restore_bulk.sh)

And it pulls that folder from /data/backups and unencrypts and uncompresses it, then puts it into /data/FOLDERNAME.restore/

*after giving a menu to ask which snapshot to use*
