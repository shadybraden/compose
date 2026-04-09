# Where Torrents are saved:

Key:

`real storage path` : `storage path shown to qbittorrent`

/data/config_storage/arr/qbittorrent:`/config`

/data/config_storage/arr/qbittorrent/complete:`/complete`

/data/mnt/torrents:`/downloads/torrents`

/data/mnt:`/allMedia`

/mnt/extra:`/mnt`

/data/dont_backup/media:`/ssd`

## Important paths to know (for saving in qbittorrent):

/downloads/torrents - where radarr and sonarr download files (they copy the files to the below folder after downloading)

/allMedia/movies - save to the Movies folder

/mnt/autobrr - the folder autobrr uses

If you download something, and set its path to `/downloads/torrents`, it will not get put into the movies/shows folder. That will only happen if radarr/sonarr do the download.

## Equivalent/Important paths in filebrowser:

Music = https://files.${DOMAIN}$`/files/data/music/` 

Movies = https://files.${DOMAIN}`/files/data/mnt/movies/`

Shows = https://files.${DOMAIN}`/files/data/mnt/shows/`

Audiobooks = https://files.${DOMAIN}`/files/data/audiobooks/`

Qbittorrent's `/downloads/torrents` = https://files.${DOMAIN}`/files/data/mnt/torrents/`
