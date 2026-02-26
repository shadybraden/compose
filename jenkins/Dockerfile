FROM jenkins/jenkins:2.541.2-lts-jdk17

USER root
RUN apt-get update
RUN apt-get install -y docker.io

# Add jenkins user to docker group with the correct GID (vie `stat -c '%g' /var/run/docker.sock`)
RUN groupmod -g 989 docker || groupadd -g 989 docker
RUN usermod -aG docker jenkins

USER jenkins
