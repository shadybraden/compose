# Discord Matrix Bridge

## Setup:

```
docker run --rm -v /data/config_storage/synapse/data/mautrix-discord:/data:z dock.mau.dev/mautrix/discord:latest
```

Then edit /data/config.yaml - see https://docs.mau.fi/bridges/general/initial-config.html

Then run (to create registration.yaml)
```
docker run --rm -v /data/config_storage/synapse/data/mautrix-discord:/data:z dock.mau.dev/mautrix/discord:latest
```

Then chown to 1337:

`sudo chown 1337:1337 registration.yaml`

`sudo chmod 0644 registration.yaml`

Then register the appservice:

https://docs.mau.fi/bridges/general/registering-appservices.html

in homeserver.yaml, add:

```yaml
app_service_config_files:
- /data/mautrix-discord/registration.yaml
```

Then restart synapse.

Then, finally, start up this container, per compose.yaml
