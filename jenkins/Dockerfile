FROM anchore/grype:v0.110.0  AS grype-builder

FROM jenkins/jenkins:2.541.3-lts-jdk17

# the path is /grype, per their own dockerfile: https://github.com/anchore/grype/blob/main/Dockerfile
COPY --from=grype-builder /grype /usr/local/bin/grype

USER jenkins
