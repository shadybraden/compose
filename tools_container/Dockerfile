FROM alpine:3.23.4

RUN apk add python3 py3-pip nodejs npm openssh curl docker-cli docker jq

# from: https://www.jeffgeerling.com/blog/2023/how-solve-error-externally-managed-environment-when-installing-pip3/
RUN rm -rf /usr/lib/python3.12/EXTERNALLY-MANAGED
RUN pip3 install ansible
