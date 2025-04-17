# Docker compose.yaml based homelab

The idea here is a single node server. With lots of containers, organization is key. This directory is where the config is. Have a poke around. Inside each folder is a `compose.yaml` file. Areas where editing is needed will be marked, but the files should be able to just be ran with `docker compose up -d`

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

- figure out how to use bitwarden cli or hashicorp vaults to fetch secrets on container start
- use [renovate](https://nickcunningh.am/blog/how-to-automate-version-updates-for-your-self-hosted-docker-containers-with-gitea-renovate-and-komodo) (and komodo) to automate updates instead of watchtower
- use some sso authentication method
- use traefik
- migrate away from monolish .env file