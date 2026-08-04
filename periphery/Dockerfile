FROM ghcr.io/moghtech/komodo-periphery:2.2.0

# Install infisical
RUN curl -L 'https://artifacts-cli.infisical.com/setup.deb.sh'  -o setup.deb.sh
RUN bash setup.deb.sh

# Install infisical
RUN apt update
RUN apt install -y infisical
