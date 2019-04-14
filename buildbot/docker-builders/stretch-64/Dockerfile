FROM debian:stretch

# Probably good to make this match what's in the master Dockerfile
ENV BUILDBOT_COMMIT dd6632af2

RUN apt-get update && apt-get -y install jq git curl wget python-dev python-numpy devscripts python-all-dev python-imaging python-pip

RUN cd /root && git clone https://github.com/buildbot/buildbot.git
RUN cd /root/buildbot && git checkout ${BUILDBOT_COMMIT} && cd /root/buildbot/slave && pip install .


ENV BUILDSLAVE_NAME diax-stretch-64
ENV BUILDSLAVE_ADMIN Nicolas Frattaroli <ovdev@fratti.ch>
ENV BUILDSLAVE_INFO Debian (stretch) 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
