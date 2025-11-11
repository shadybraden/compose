# Matrix

Setup:
```
docker run -it --rm \
    -v /data/config_storage/synapse/data:/data \
    -e SYNAPSE_SERVER_NAME=matrix.holmlab.org \
    -e SYNAPSE_REPORT_STATS=no \
    matrixdotorg/synapse:latest generate
```