FROM anchore/grype:v0.111.1  AS grype-builder

FROM jenkins/jenkins:2.541.3-lts-jdk21

# the path is /grype, per their own dockerfile: https://github.com/anchore/grype/blob/main/Dockerfile
COPY --from=grype-builder /grype /usr/local/bin/grype

USER jenkins
