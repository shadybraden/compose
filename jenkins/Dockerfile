FROM anchore/grype:v0.109.1  AS grype-builder

FROM jenkins/jenkins:2.541.2-lts-jdk17

# the path is /grype, per their own dockerfile: https://github.com/anchore/grype/blob/main/Dockerfile
COPY --from=grype-builder /grype /usr/local/bin/grype

USER jenkins
