# email archive

https://github.com/rustmailer/bichon/wiki/Using-Bichonctl-For-Email-Import

```
cd /data/config_storage/email_archive
docker run -it --rm -v $(pwd):/mnt rustmailer/bichon bichonctl
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
