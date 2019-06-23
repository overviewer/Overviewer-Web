FROM python:3.5

COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

RUN apt-get update && apt-get install -y gnupg-agent dpkg-sig createrepo rpm expect

COPY master /root/master
COPY repos /root/repos
COPY start.sh codesign.asc rpmsign.sh /root/

RUN gpg --import --batch /root/codesign.asc && rm /root/codesign.asc

CMD /root/start.sh
VOLUME /data/buildbot
EXPOSE 9989
EXPOSE 8010
