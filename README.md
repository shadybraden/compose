# Docker compose.yaml based homelab

re-write coming...ssh edit

This is an opinionated homelab. It is a single server that is GitOps'ed and version controlled

Read

Inside each folder is a `compose.yaml` file. Areas where editing is needed will be marked, but the files should be able to just be ran with `docker compose up -d`

Remember; if there is a file (for example `settings.json`) in the volumes section of any docker-compose.yml, then that file has to already exist.
So make sure to run `touch settings.json` first, or docker will make the *FOLDER* `settings.json` instead of the file.

See each folder's README for details on what each thing is and what it does.

# How to use this repo:

1. `git clone https://github.com/shadybraden/compose.git` 
2. `cd compose/` 
3. `cp .env.sample .env`
4. Now use `nano .env` (or any other text editor) to edit the file `.env` and add in your environment variables. The defaults will allow the container to function, but may not be ideal. For example, all passwords and secrets are simply "password". Once you edit this file, or at any point, run `sudo chmod 600 .env && sudo chown root:root .env` to secure it a bit more. (note that this works with docker and *probably not* podman)
5. Once the `.env` file is setup as desired, `cd <container name>` and see the README.md for that container's specific instructions.
6. Once satisfied, run this to start the container: `docker compose --env-file ../.env -v up -d` 
7. Now if you want to pull the latest, run `git pull` then compare the latest in `.env.sample` to your `.env` 

---

### Roadmap:

- komodo
- renovate
- traefik
- figure out how to use bitwarden cli or hashicorp vaults to fetch secrets on container start
- use some sso authentication method
- migrate away from monolith .env file
- doc on order of setup. (pihole, traefik auth etc)