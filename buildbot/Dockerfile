#FROM python:3.10
# We need this because jammy's dpkg supports zstd and bullseye's doesn't
FROM ubuntu:jammy

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y gnupg-agent dpkg-sig createrepo-c rpm\
    expect python3 python3-pip libpq-dev

COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt


COPY master /root/master
COPY repos /root/repos
COPY start.sh codesign.asc rpmsign.sh /root/

RUN gpg --import --batch /root/codesign.asc && rm /root/codesign.asc

CMD /root/start.sh
VOLUME /data/buildbot
EXPOSE 9989
EXPOSE 8010
