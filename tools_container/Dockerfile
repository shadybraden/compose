FROM alpine:3.23.4

RUN apk add python3=3.12.13-r0
RUN apk add py3-pip=25.1.1-r1
RUN apk add nodejs=24.14.1-r0
RUN apk add  npm=11.11.0-r0
RUN apk add openssh=10.2_p1-r0

RUN rm -rf /usr/lib/python3.12/EXTERNALLY-MANAGED
RUN pip3 install ansible==13.6.0
