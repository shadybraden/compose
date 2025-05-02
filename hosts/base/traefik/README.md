# Reverse Proxy

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-official-docker-image

## Vars to change:

TRAEFIK_DASHBOARD_CREDENTIALS
CF_DNS_API_TOKEN
CF_API_EMAIL

traefik.yml and config.yml are set as hidden files. run `cp .traefik.yml.sample traefik.yml` & `cp .config.yml.sample config.yml`

---

## Sample yaml to add to a container.

Find and replace STACKNAME

```yaml
    security_opt:
      - no-new-privileges:true # helps to increase security
    networks:
      - intranet
    labels:
    - "traefik.enable=true"
    - "traefik.http.routers.STACKNAME.entrypoints=http"
    - "traefik.http.routers.STACKNAME.rule=Host(`STACKNAME.holmlab.org`)"
    - "traefik.http.middlewares.STACKNAME-https-redirect.redirectscheme.scheme=https"
    - "traefik.http.routers.STACKNAME.middlewares=STACKNAME-https-redirect"
    - "traefik.http.routers.STACKNAME-secure.entrypoints=https"
    - "traefik.http.routers.STACKNAME-secure.rule=Host(`STACKNAME.holmlab.org`)"
    - "traefik.http.routers.STACKNAME-secure.tls=true"
    - "traefik.http.routers.STACKNAME-secure.service=STACKNAME"
    - "traefik.http.services.STACKNAME.loadbalancer.server.port=80" # port of the service. i.e. STACKNAME likes 9000
    - "traefik.docker.network=intranet"

networks:
  intranet:
    external: true
```