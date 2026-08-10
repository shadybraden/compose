# email archive

https://github.com/rustmailer/bichon/wiki/Using-Bichonctl-For-Email-Import

## Import emails to Bichon NoSync account

```
cd /data/config_storage/email_archive
docker run -it --rm -v $(pwd):/mnt rustmailer/bichon bichon-cli
```

- [ ] Enter url `https://bichon.holmlab.org/`
- [ ] Enter your api token (create here: https://bichon.holmlab.org/settings/api-tokens)
- [ ] Don't save
- [ ] Select the no-sync account (already made manually)
- [ ] EML scan recursivly
- [ ] Enter root: `/mnt`
- [ ] Profit

## Migrate from 0.3.7 to 1.0.0

`cd /data/config_storage/email_archive`

`docker run -it --rm -v $(pwd):/data rustmailer/bichon bichon-admin`

## Migrate from 1.x to 2.0.0

https://github.com/rustmailer/bichon/wiki/Bichon-v2.x-Migration-Guide#migration-path-b-v1x--v2x

`cd /data/config_storage/compose/bichon` 

`docker compose run bichon bichon-admin` 

- select migration step
- root dir is `/data`
- data dir is `/data`
- batch size default

confirm: `cat /data/config_storage/bichon/STORAGE_VERSION` should show `2` 
