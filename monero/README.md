# Monero miner and node

If you dont have an address:

- download a client: https://www.getmonero.org/downloads/
- make a wallet and get its recieve address

https://hub.docker.com/r/miningcontainers/xmrig


## If you don't want to use a VPN while using this, replace the docker-compose.yml contents with the below:

```yml
services:
  xmrig:
    restart: unless-stopped
    container_name: xmrig
    image: miningcontainers/xmrig
    deploy:
        resources:
            limits:
                cpus: "${monero_cpu_limit}"
    command: -k --tls -o pool.hashvault.pro:443 -u ${monero_address} --donate-level 1 --tls --tls-fingerprint 420c7850e09b7c0bdcf748a7da9eb3647daf8515718f36d9ccfdd6b9ff834b14
```