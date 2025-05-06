# Backup your homelab

There are two folders of interest
`/data/config_storage`
`/mnt/4tb/immich` - this will become `/mnt/important_data` one day...

The goal is to take `frequent` snapshot backups of `/data/config_storage` and `infrequent` ones of `/mnt/4tb/immich`

## Frequent backups

Backed up data will live in `/data/backups`. It will be moved to various locations via...

We will use Restic for this as it compresses and encrypts the backed up data.
