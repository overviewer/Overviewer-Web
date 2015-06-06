FROM python:2.7

ENV BUILDBOT_COMMIT dd6632af2

#RUN pip install buildbot
RUN cd /root && git clone https://github.com/buildbot/buildbot.git
RUN cd /root/buildbot/master && git checkout ${BUILDBOT_COMMIT} && pip install . && pip install psycopg2==2.6 && pip install itsdangerous

RUN apt-get update && apt-get install -y gnupg-agent dpkg-sig

COPY start.sh master.cfg codesign.asc /root/
RUN gpg --import /root/codesign.asc && rm /root/codesign.asc

COPY debian_control_files/all.tar /root/debian.tar

CMD /root/start.sh
VOLUME /data/buildbot
EXPOSE 9989
EXPOSE 8010
