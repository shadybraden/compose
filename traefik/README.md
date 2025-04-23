# Reverse Proxy

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-official-docker-image

```yaml
    security_opt:
      - no-new-privileges:true # helps to increase security
    networks:
      - intranet
    labels:
    - "traefik.enable=true"
    - "traefik.http.routers.pihole.entrypoints=http"
    - "traefik.http.routers.pihole.rule=Host(`pihole.holmlab.org`)"
    - "traefik.http.middlewares.pihole-https-redirect.redirectscheme.scheme=https"
    - "traefik.http.routers.pihole.middlewares=pihole-https-redirect"
    - "traefik.http.routers.pihole-secure.entrypoints=https"
    - "traefik.http.routers.pihole-secure.rule=Host(`pihole.holmlab.org`)"
    - "traefik.http.routers.pihole-secure.tls=true"
    - "traefik.http.routers.pihole-secure.service=pihole"
    - "traefik.http.services.pihole.loadbalancer.server.port=80" # port of the service. i.e. pihole likes 9000
    - "traefik.docker.network=intranet"

networks:
  intranet:
    external: true
```