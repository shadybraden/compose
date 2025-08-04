#!/bin/bash

SERVERNAME=$1
SERVICE=$2

TOML_BLOCK=$(cat <<EOF

##

[[stack]]
name = "$SERVICE-$SERVERNAME"
tags = ["$SERVERNAME", "unhooked", "criticality: 1"]
[stack.config]
server = "$SERVERNAME"
project_name = "$SERVICE-$SERVERNAME"
git_provider = "git.holmlab.org"
git_account = "komodo"
repo = "shady/compose"
branch = "main"
run_directory = "$SERVICE"
additional_env_files = ["/etc/komodo/domain.env"]
EOF
)

echo "$TOML_BLOCK" >> syncs/$SERVERNAME.toml
