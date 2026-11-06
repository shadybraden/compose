# AGENTS.md

Guidance for AI agents working in this repo. Read this before changing anything that touches maul.

## What this repo is

A compose-based homelab. Two deployment targets share the repo:

- **Maul (podman, this doc's focus).** Fedora CoreOS host at `10.1.1.69`, deployed by Ansible from Forgejo Actions. Service folders named `*-podman` (plus `chhoto-url`, `shadybradencom` and others) are the maul containers. Their compose files are rootless podman compose.
- **Docker hosts (Komodo).** The other service folders (`dozzle/`, `homepage/`, `tinyauth/`, `traefik/`, etc.) are Docker compose for the Komodo-managed hosts. Their compose files often reference Komodo paths such as `/data/config_storage/komodo/...`. The separate IaC repo is what Komodo deploys from; this repo is the podman side of the same homelab. Do not switch a Komodo compose file to podman unless asked. Create a `-podman` copy instead.

## Maul

- **Host:** Fedora CoreOS, `10.1.1.69`. The same IP is used for two Ansible users, `core` and `maul`.
- **Users:** `maul` runs rootless podman and owns the service data. `core` runs the host-level Ansible tasks (`rpm-ostree`, sysctl, reboots).
- **SSH:** key-only (`PasswordAuthentication no`, `PermitRootLogin no`), `AllowUsers core maul`, `MaxAuthTries 3`. SSH is only allowed from `10.1.1.0/24` by firewalld.
- **Semi-airgapped:** the host cannot reach `docker.io`, `git.holmlab.org`, or `infisical.holmlab.org` directly. Egress is forced through the squid proxy at `10.1.1.65:3128`, which only allows CONNECT to a short allowlist (Fedora, Quay, Let's Encrypt, Cloudflare API). Anything else from maul must be pulled by the CI runner and transferred.
- **Proxy handling:** `/etc/profile.d/proxy.sh` sets `http(s)_proxy` with `NO_PROXY` for `localhost`, `maul.shadybraden.com`, and `.maul.shadybraden.com`. Podman passes host proxy variables into containers, so containers that call each other need `NO_PROXY` too. `traefik-podman` sets `NO_PROXY` for `tinyauth`, `10.89.0.0/24` (intranet), `10.90.0.0/24` (intranet-backend), and the maul domains. Traefik calls backends by container IP, so the CIDRs matter, not just names.
- **Networks:**
  - `intranet`: `10.89.0.0/24`, external, created by `playbooks/maul.yaml`.
  - `intranet-backend`: `10.90.0.0/24`, internal (no egress), created by `playbooks/maul.yaml`.
  - Traefik is on both. Backend containers that Traefik should route to are on `intranet-backend` and set `traefik.docker.network=intranet-backend`.
- **Boot:** linger is enabled for `maul` (butane writes `/var/lib/systemd/linger/maul`). `podman-restart.service` and `podman.socket` are enabled by `playbooks/maul.yaml`. Containers with `restart: unless-stopped` come back after reboot only because of `podman-restart`.
- **Podman socket:** `${XDG_RUNTIME_DIR}/podman/podman.sock` (`/run/user/<uid>/podman/podman.sock`) is the Docker-compatible socket. Traefik, Dozzle, and Homepage mount it as `/var/run/docker.sock`. Those containers need `label=disable` for SELinux.

## butane.yaml

`butane.yaml` is the source for the FCOS first-boot config (`config.ign` is its generated output). It defines:

- the `maul` and `core` users and their SSH keys
- sshd hardening (`/etc/ssh/sshd_config.d/10-hardening.conf`)
- zincati update strategy and window
- proxy settings for zincati, rpm-ostreed, the FCOS pinger, and `/etc/profile.d/proxy.sh`
- `firewalld` zone and direct rules: outbound only to the proxy, NTP, and established traffic; everything else dropped; `FORWARD` from `10.89.0.0/24` only to the proxy
- `/etc/selinux/config` (enforcing), `/etc/hostname` (`maul`), linger for `maul`

Ignition only runs on first boot. Changing `butane.yaml` does not change a running host. Edit the live file on the host, or re-provision. Keep `config.ign` in sync with `butane.yaml` when regenerating it.

## CI/CD: `.forgejo/workflows/maul.yaml`

Runs on `tools_container`. Triggers on push to `main` and on `workflow_dispatch` (with a `service` choice, `none` skips deploys).

See IaC repo (typically at .,/IaC) for `tools_container` Dockerfile and build. TLDR: its dind, with some tools installed (curl, infisical cli, etc)
 
`concurrency: maul-deploy` with `cancel-in-progress: false`, so runs queue instead of cancelling each other.

Jobs, in order:

1. **Core**: runs `playbooks/core.yaml` with `CORE_SSH_PRIVATE_KEY`. Bootstraps python3 and podman-compose with `rpm-ostree`, reboots if needed, and installs sysbench and btop. Reboots the host when packages change.
2. **Maul**: needs Core. Runs `playbooks/maul.yaml` with `MAUL_SSH_PRIVATE_KEY`. Creates the networks, enables the podman socket and `podman-restart`, refreshes the shared repos (`icons` → `~/icons`, `shadybradencom` → `~/shadybradencom`), transfers and builds the hugo site, and prints the OS version.
3. **Detect**: needs Maul. Works out which services to deploy.
   - Manual dispatch: the `service` input.
   - Push: every changed `*/compose.yaml` whose directory name is in `MAUL_SERVICES`.
4. **Maul-Services**: needs Detect, runs only when Detect found something. Runs `playbooks/maul_service.yaml -e service=<name>` for each.

**`MAUL_SERVICES` is the list of main podman containers.** Currently: `chhoto-url traefik-podman tinyauth-podman homepage-podman dozzle-podman shadybradencom`. Adding a service means adding its directory name to `MAUL_SERVICES` and to the `options` list of the `service` input. Both places must match.

Failure notifications go to ntfy via `NTFY_TOPIC`.

## Deploying a service: `playbooks/maul_service.yaml`

For each service name, the runner:

1. Reads `<service>/compose.yaml` and collects the `image:` values.
2. Pulls each image on the runner, saves it to an archive in `RUNNER_TEMP`, copies it to maul, and loads it (maul cannot reach registries).
3. Logs in to Infisical with `INFISICAL_MAUL_*` secrets and exports two paths: the shared root `/` (for example `DOMAIN`) and `/<service>`. Service values override shared ones. If the service folder doesn't exist in Infisical, the service export is skipped and only `/` is used. Writes the result to `<service>/.env` with mode `0600`.
4. Copies the whole `<service>/` folder to `~/config_storage/<service>/` on maul.
5. Creates per-service state directories where needed (`traefik-podman`: `acme.json` `0600` and `logs`; `homepage-podman`: `logs` `0777`; `dozzle-podman`: `data` `0777`).
6. Runs `XDG_RUNTIME_DIR=/run/user/$(id -u) podman compose -f ~/config_storage/<service>/compose.yaml up -d`.

Notes:

- Compose files need their `.env` values in Infisical (at the service path or `/`), or interpolation will be empty.
- Config files copied with `copy` keep their repo permissions. Secrets are only in `.env`.

## Shared repos

`playbooks/maul.yaml` defines `shared_repos`. `playbooks/tasks/maul_repo.yaml` clones each repo on the runner when `main`'s commit differs from the one recorded in `~/.revisions/<name>`, clears the destination, and copies the files to maul. `.git` is not copied.

## Hugo site

- The hugo source is `~/shadybradencom` (repo `shadybradencom`).
- `playbooks/maul.yaml` transfers `hugomods/hugo:0.165.0` if it isn't on maul, then builds with `podman run` into `~/config_storage/shadybradencom/public`.
- `shadybradencom/compose.yaml` is nginx serving that `public` folder on `intranet-backend` (listening on 8088). Traefik routes `${DOMAIN}` (the bare domain, `maul.shadybraden.com` on maul) to it.
- `hugo-builder/` is a leftover from the Komodo setup. Not used on maul.

## Traefik on maul (`traefik-podman/`)

- Only HTTPS on `:443`. No `http` entrypoint, no port 80, no HTTP-to-HTTPS redirect. Don't add HTTP routers to maul services.
- Routers come from container labels via the docker provider (the podman socket). `config.yaml` (file provider) holds only the `default-security-headers` middleware and the dashboard is `api@internal` behind basic auth.
- TLS: Let's Encrypt via Cloudflare DNS challenge. `CF_DNS_API_TOKEN`, `CF_API_EMAIL` come from `.env`. The ACME email is set with `TRAEFIK_CERTIFICATESRESOLVERS_CLOUDFLARE_ACME_EMAIL` (no email in `traefik.yaml`).
- `exposedByDefault: false`: every routed container needs `traefik.enable=true`.
- Backend TLS verification is on. `crafty` is the only transport with `insecureSkipVerify`.

## Auth: ForwardAuth per container

Tinyauth is not a Traefik middleware in `config.yaml`. Each service that needs login defines its own middleware in its labels, named `<service>-tinyauth`:

```
traefik.http.middlewares.<service>-tinyauth.forwardauth.address=http://tinyauth:3000/api/auth/traefik
traefik.http.middlewares.<service>-tinyauth.forwardauth.trustforwardheader=false
traefik.http.middlewares.<service>-tinyauth.forwardauth.maxresponsebodysize=1048576
traefik.http.routers.<service>-secure.middlewares=<service>-tinyauth
```

Tinyauth itself is not behind ForwardAuth. If tinyauth is down, every protected service fails.

## Conventions for maul compose files

- File is `<service>/compose.yaml`. Folder name = service name = `MAUL_SERVICES` entry.
- Secrets live in Infisical, not in the repo. `.env` and `*.env` are gitignored.
- Bind mounts are relative to the compose file (`./config.yaml`). Use `:z` on mounts for SELinux. Use `label=disable` (in `security_opt`) for the podman socket.
- Quote `"no"` for `restart`. An unquoted `no` is parsed as YAML `false`.
- No `dns:` blocks. No `http` entrypoint routers. No `anubis`.
- `tmpfs` takes only `size` and `mode` (`uid=`/`gid=` are rejected by podman).
- Don't set `ulimits.nproc`. It counts every process the `maul` user runs and makes `crun` fail with `clone: Resource temporarily unavailable`.
- Non-root containers can't bind ports below 1024 (`cap_drop: ALL`). Listen on a high port inside the container and set the Traefik `loadbalancer.server.port` to match.
- Timezone: `TZ: America/New_York` in the environment. Don't mount `/etc/localtime` (it's missing on FCOS).
- Use `intranet` for services that Traefik should reach by default, `intranet-backend` for backends that shouldn't have egress.

## Known pitfalls

- A bind mount to a path that doesn't exist yet is created as a **directory** by podman. Create files like `acme.json` before the container starts.
- Repos cloned on the runner must be copied, not moved. `.git` is stripped before copying.
- Running `podman restart` doesn't pick up a changed compose file. Redeploy through the workflow or `podman compose up -d`.
- Traefik's docker provider can miss containers that start after it's running. If a router doesn't appear in the dashboard, restart the affected container, then check `/api/http/routers`.
- Never try to SSH into any of these machines (maul, core, or any other host). Access is not available to agents. Ask the user to run commands on the host instead.
- Traefik does not post its logs to `podman logs`. Read them from the files on maul: `~/config_storage/traefik-podman/logs/traefik.log` (service log) and `~/config_storage/traefik-podman/logs/access.log` (access log).
- Times in `ls -l` and logs differ between host (UTC) and containers (`America/New_York`). Compare timestamps in the same timezone.
- The squid proxy denies everything outside its allowlist with a plain `403` and `x-squid-error: ERR_ACCESS_DENIED`. If a service gets that response, a process is going through the proxy instead of connecting directly.
- Healthchecks that call `localhost` fail on maul unless the container sets `NO_PROXY=localhost` and `no_proxy=localhost`. The host's proxy variables send the check through squid, the check fails, and Traefik skips the container, so its router never appears. Any container with a `curl` healthcheck needs these vars.

## Editing this file

Update this file when maul's config changes: new services in `MAUL_SERVICES`, new networks, new shared repos, new Ansible tasks, or changes to the proxy, firewall, or auth model.
