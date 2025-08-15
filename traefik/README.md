# Reverse Proxy

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-official-docker-image

## Vars to change:

TRAEFIK_DASHBOARD_CREDENTIALS

CF_DNS_API_TOKEN

CF_API_EMAIL

---

Set these, and save them. For starting a new homelab, start Traefik from anywhere, and hand it off to Komodo once it is setup.

For an additional server deployment, make the files below, then use Komodo to set the env vars.

## Make files

`cd /data/config_storage && git clone https://git.holmlab.org/shady/compose.git`

`cp /data/config_storage/compose/traefik/traefik.yaml.sample /data/config_storage/traefik/traefik.yml`

`touch /data/config_storage/traefik/acme.json && chmod 600 /data/config_storage/traefik/acme.json`

Then edit `/data/config_storage/traefik/traefik.yml` as needed (should be just email)

---

## Sample yaml to add to a container.

Change port and SUBDOMAIN as needed

```yaml
    security_opt:
      - no-new-privileges:true  # helps to increase security
    networks:
      - intranet
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.SUBDOMAIN.entrypoints=http"
      - "traefik.http.routers.SUBDOMAIN.rule=Host(`SUBDOMAIN.${DOMAIN}`)"
      - "traefik.http.middlewares.SUBDOMAIN-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.SUBDOMAIN.middlewares=SUBDOMAIN-https-redirect"
      - "traefik.http.routers.SUBDOMAIN-secure.entrypoints=https"
      - "traefik.http.routers.SUBDOMAIN-secure.rule=Host(`SUBDOMAIN.${DOMAIN}`)"
      - "traefik.http.routers.SUBDOMAIN-secure.tls=true"
      - "traefik.http.routers.SUBDOMAIN-secure.service=SUBDOMAIN"
      - "traefik.http.services.SUBDOMAIN.loadbalancer.server.port=80"  # port of the service.
      - "traefik.docker.network=intranet"

networks:
  intranet:
    external: true

```

To include something to TinyAuth:
```yaml
      - "traefik.http.routers.SERVICENAME-secure.middlewares=tinyauth"
```

To use Anubis:
```
      - traefik.http.routers.SUBDOMAIN.middlewares=anubis@docker
```

To add to Homepage:
```yaml
      - "homepage.group=GROUP"
      - "homepage.name=NAME"
      - "homepage.icon=/images/NAME.png"
      - "homepage.href=https://NAME.${DOMAIN}/"
```