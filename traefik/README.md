# Reverse Proxy

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-official-docker-image

## Vars to change:

TRAEFIK_DASHBOARD_CREDENTIALS
CF_DNS_API_TOKEN
CF_API_EMAIL

traefik.yml and config.yml are set as hidden files. run `cp .traefik.yml.sample /data/config_storage/traefik/traefik.yml` & `cp .config.yml.sample /data/config_storage/traefik/config.yml`

also `touch /data/config_storage/traefik/acme.json`

all together:

```shell
mkdir /data/config_storage/traefik
cp .traefik.yml.sample /data/config_storage/traefik/traefik.yml && \
touch /data/config_storage/traefik/acme.json
chmod 600 /data/config_storage/traefik/acme.json
ls -Al /data/config_storage/traefik
```

Then edit `/data/config_storage/traefik/traefik.yml`

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
    - "traefik.http.routers.${SUBDOMAIN}.entrypoints=http"
    - "traefik.http.routers.${SUBDOMAIN}.rule=Host(`${SUBDOMAIN}.${DOMAIN}`)"
    - "traefik.http.middlewares.${SUBDOMAIN}-https-redirect.redirectscheme.scheme=https"
    - "traefik.http.routers.${SUBDOMAIN}.middlewares=${SUBDOMAIN}-https-redirect"
    - "traefik.http.routers.${SUBDOMAIN}-secure.entrypoints=https"
    - "traefik.http.routers.${SUBDOMAIN}-secure.rule=Host(`${SUBDOMAIN}.${DOMAIN}`)"
    - "traefik.http.routers.${SUBDOMAIN}-secure.tls=true"
    - "traefik.http.routers.${SUBDOMAIN}-secure.service=${SUBDOMAIN}"
    - "traefik.http.services.${SUBDOMAIN}.loadbalancer.server.port=80" # port of the service.
    - "traefik.docker.network=intranet"

networks:
  intranet:
    external: true
```