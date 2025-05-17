# Docker compose.yaml based homelab

This is an opinionated homelab. It is a [single server](https://aoostar.com/products/aoostar-r1-2bay-nas-intel-n100-mini-pc-with-w11-pro-lpddr4-16gb-ram-512gb-ssd) (can do more) that is GitOps'ed and version controlled
Inside each folder is a `compose.yaml` file. Read the readme, and edit the .env.sample as needed.
It can be used simply as individual containers and you can connect to and use each with its port and ip. However, following [the guide here](https://shadybraden.com/articles/gitopshomelab/) is the recomended way of running this homelab
As the guide says, installing OS's, using Git and using Docker are prerequisites and fundamental knowlege.

---

### todo:

- https://github.com/renovatebot/renovate/discussions/13052 fix linuxserver.io image versioning
- https://github.com/almeidapaulopt/tsdproxy for multi device managment
- swap subdomain and domain with vars? see adsb