#!/bin/bash

SERVERNAME=$1
SERVICE=$2

TOML_BLOCK=$(cat <<EOF

##

[[stack]]
name = "$SERVICE-$SERVERNAME"
tags = ["$SERVERNAME", "criticality: 1"]
[stack.config]
server = "$SERVERNAME"
project_name = "$SERVICE-$SERVERNAME"
linked_repo = "compose_main"
run_directory = "$SERVICE"
additional_env_files = ["/etc/komodo/domain.env"]
env_file_path = "/etc/komodo/env/$SERVICE-$SERVERNAME.env"
EOF
)

echo "$TOML_BLOCK" >> ../IaC/syncs/$SERVERNAME.toml
