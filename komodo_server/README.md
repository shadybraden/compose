`cp compose.env.sample compose.env`

using stacks like:

https://nickcunningh.am/blog/how-to-automate-version-updates-for-your-self-hosted-docker-containers-with-gitea-renovate-and-komodo

sets the storage location of compose.yaml to `/etc/komodo/stacks/test_stack/ntfy/`


edit these vars in `.env`:
KOMODO_DB_PASSWORD
KOMODO_PASSKEY
KOMODO_WEBHOOK_SECRET
KOMODO_JWT_SECRET