# Resource Syncs for Komodo

Setup syncs.toml and the rest will be imported.

Don't forget webhooks!

---

#### A note about env vars:

How I add passwords or things I don't want in my public git repo:

- in any compose.yaml, have a ${password}
- Go to the web ui > Stacks > Environment and manually paste in `password=aReallyGoodPassword`

This is great and works well. However, there are times when I want to put an env into code. On redeploy, the codified vars overwite the manually configured ones, and delete them.

So, env files.

In /data/config_storage/komodo/etc_komodo I have files like this: `holmlaborg.env`. Inside them is: `DOMAIN=holmlab.org`

So add the following to the syncs toml:

```
additional_env_files = ["/etc/komodo/holmlaborg.env"]
```
