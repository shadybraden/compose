# Sample yaml to add to a container.

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
      - "traefik.http.routers.SUBDOMAIN-secure.middlewares=tinyauth"
```

To use Anubis:
```yaml
      - "traefik.http.routers.SUBDOMAIN.middlewares=anubis@docker"
```

To add to Homepage:
```yaml
      - "homepage.group=Other"
      - "homepage.name=SUBDOMAIN"
      - "homepage.icon=/images/SUBDOMAIN.png"
      - "homepage.href=https://SUBDOMAIN.${DOMAIN}/"
```

---

# Sample yaml to add to a container connecting to Gluetun:

To add to Traefik, add this to `gluetun/compose.yaml` 
```yaml
      - "traefik.http.routers.SUBDOMAIN.entrypoints=http"
      - "traefik.http.routers.SUBDOMAIN.rule=Host(`SUBDOMAIN.${DOMAIN}`)"
      - "traefik.http.middlewares.SUBDOMAIN-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.SUBDOMAIN.middlewares=SUBDOMAIN-https-redirect"
      - "traefik.http.routers.SUBDOMAIN-secure.entrypoints=https"
      - "traefik.http.routers.SUBDOMAIN-secure.rule=Host(`SUBDOMAIN.${DOMAIN}`)"
      - "traefik.http.routers.SUBDOMAIN-secure.tls=true"
      - "traefik.http.routers.SUBDOMAIN-secure.service=SUBDOMAIN"
      - "traefik.http.services.SUBDOMAIN.loadbalancer.server.port=8080"  # port of the service.
```

To add to homepage
```yaml
    security_opt:
      - no-new-privileges:true  # helps to increase security
    labels:
      - "homepage.group=SUBDOMAIN"
      - "homepage.name=SUBDOMAIN"
      - "homepage.icon=/images/SUBDOMAIN.png"
      - "homepage.href=https://SUBDOMAIN.${DOMAIN}/"

```
