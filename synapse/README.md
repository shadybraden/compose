# Matrix

Setup:
```
docker run -it --rm \
    -v /data/config_storage/synapse/data:/data \
    -e SYNAPSE_SERVER_NAME=matrix.holmlab.org \
    -e SYNAPSE_REPORT_STATS=no \
    matrixdotorg/synapse:latest generate
```

Generate admin (https://github.com/element-hq/synapse/blob/develop/docker/README.md#generating-an-admin-user)
```
docker exec -it synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -a
```

Generate user
```
docker exec -it synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml --no-admin
```
