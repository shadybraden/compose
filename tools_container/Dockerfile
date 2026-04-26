FROM alpine:3.22.4

RUN apk add python3 py3-pip nodejs npm openssh curl

RUN rm -rf /usr/lib/python3.12/EXTERNALLY-MANAGED
RUN pip3 install ansible
