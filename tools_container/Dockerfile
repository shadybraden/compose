FROM alpine:3.23.4

RUN apk add python3=3.12.13-r0

RUN rm -rf /usr/lib/python3.12/EXTERNALLY-MANAGED
RUN apk add py3-pip=25.1.1-r1

RUN pip3 install ansible==13.6.0
