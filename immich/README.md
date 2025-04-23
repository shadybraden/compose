# Photo storage

this needs to be added to traefik.yml:
```yml
entryPoints:
  websecure:
    address: :443
    # this section needs to be added
    transport:
      respondingTimeouts:
        readTimeout: 600s
        idleTimeout: 600s
        writeTimeout: 600s
```