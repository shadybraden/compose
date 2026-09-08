# Docker compose.yaml based homelab

This is an opinionated homelab. It is a [single server](https://aoostar.com/products/aoostar-r1-2bay-nas-intel-n100-mini-pc-with-w11-pro-lpddr4-16gb-ram-512gb-ssd) (can do more) that is GitOps'ed and version controlled
Inside each folder is a `compose.yaml` file. Read the readme, and edit the .env.sample as needed.
It can be used simply as individual containers and you can connect to and use each with its port and ip. However, following [the guide here](https://shadybraden.com/articles/gitopshomelab/) is the recommended way of running this homelab.
As the guide says, installing OS's, using Git and using Docker are prerequisites and fundamental knowledge.

---

### todo:

- Buddy backup system
- [anubis + traefik](https://anubis.techaro.lol/docs/admin/environments/traefik) --> [wait for middlewares](https://git.holmlab.org/shady/compose/src/branch/main/anubis/README.md) 
- Orchestrate Talos

---

# Adding a service:

`./addservice.sh <server_name> <service_name>`

<details>
<summary>Traefik</summary>

## Sample yaml to add to a container to add it to Traefik

#### Change port and SUBDOMAIN as needed

```yaml
    dns:
      - ${DNS_SERVER1}
      - ${DNS_SERVER2}
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
      - "traefik.http.routers.SUBDOMAIN-secure.middlewares=internal-only"
      - "traefik.http.routers.SUBDOMAIN-secure.tls=true"
      - "traefik.http.routers.SUBDOMAIN-secure.service=SUBDOMAIN"
      - "traefik.http.services.SUBDOMAIN.loadbalancer.server.port=80"  # port of the service.
      - "traefik.docker.network=intranet"

networks:
  intranet:
    external: true

```

`internal-only` is defined by the Traefik stack. Its allowlist includes the
`10.1.1.0/24` LAN, Tailscale address ranges, loopback, and Docker bridge
networks. Adjust its `ipallowlist.sourcerange` label in
`traefik/compose.yaml` if those networks change.
</details>

<details>
<summary>To expose a service publicly:</summary>

Set `PUBLIC_DOMAIN` in the service's Komodo variables or `.env` file, then add
these labels alongside its existing internal Traefik labels. The public router
must not use the `internal-only` middleware.

```yaml
      - "traefik.http.routers.SUBDOMAIN-public.entrypoints=http"
      - "traefik.http.routers.SUBDOMAIN-public.rule=Host(`SUBDOMAIN.${PUBLIC_DOMAIN}`)"
      - "traefik.http.routers.SUBDOMAIN-public.middlewares=SUBDOMAIN-https-redirect"
      - "traefik.http.routers.SUBDOMAIN-public-secure.entrypoints=https"
      - "traefik.http.routers.SUBDOMAIN-public-secure.rule=Host(`SUBDOMAIN.${PUBLIC_DOMAIN}`)"
      - "traefik.http.routers.SUBDOMAIN-public-secure.tls=true"
      - "traefik.http.routers.SUBDOMAIN-public-secure.service=SUBDOMAIN"
```

The Traefik stack requests `${PUBLIC_DOMAIN}` and `*.${PUBLIC_DOMAIN}` using the
Cloudflare DNS challenge. Its API token must have DNS edit access to both domain
zones. Point the public hostname (or a wildcard DNS record) at the WAN address
and forward TCP ports 80 and 443 to Traefik. Some applications also need their
external URL or allowed-host setting changed to the public hostname.
</details>

<details>
<summary>Additional security improvments: (these will break stuff)</summary>

```yaml
    tmpfs:
      - '/tmp:size=64m'
    read_only: true
    cap_add:
      - NET_BIND_SERVICE
    cap_drop:
      - ALL
    init: true
```
</details>

<details>
<summary>To include something to TinyAuth:</summary>

```yaml
      - "traefik.http.routers.SUBDOMAIN-secure.middlewares=tinyauth,internal-only"
```
</details>

<details>
<summary>To use Anubis:</summary>

```yaml
      - "traefik.http.routers.SUBDOMAIN.middlewares=anubis@docker"
```
</details>

<details>
<summary>To add to Homepage:</summary>

```yaml
      - "homepage.group=Other"
      - "homepage.name=SUBDOMAIN"
      - "homepage.icon=/images/SUBDOMAIN.png"
      - "homepage.href=https://SUBDOMAIN.${DOMAIN}/"
```
</details>

<details>
<summary>Gluetun:</summary>

## Sample yaml to add to a container connecting to Gluetun:

#### To add to Traefik, add this to `gluetun/compose.yaml`:

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

#### To add to homepage for `SERVICE/compose.yaml`:

```yaml
    security_opt:
      - no-new-privileges:true  # helps to increase security
    network_mode: container:gluetun
    labels:
      - "homepage.group=SUBDOMAIN"
      - "homepage.name=SUBDOMAIN"
      - "homepage.icon=/images/SUBDOMAIN.png"
      - "homepage.href=https://SUBDOMAIN.${DOMAIN}/"

```
</details>
