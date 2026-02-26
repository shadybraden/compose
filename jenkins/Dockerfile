FROM anchore/grype:v0.109.0  AS grype-builder

FROM jenkins/jenkins:2.541.2-lts-jdk17

COPY --from=grype-builder /grype /usr/local/bin/grype

USER root
RUN apt-get update
RUN apt-get install -y docker.io

USER jenkins
