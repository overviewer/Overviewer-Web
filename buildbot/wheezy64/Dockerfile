FROM debian:wheezy
#FROM luisalejandro/debian-i386

# Probably good to make this match what's in the master Dockerfile
ENV BUILDBOT_COMMIT dd6632af2

RUN apt-get update && apt-get -y install git curl python-dev python-numpy devscripts python-all-dev python-imaging && curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python2

RUN cd /root && git clone https://github.com/buildbot/buildbot.git
RUN cd /root/buildbot/slave && git checkout ${BUILDBOT_COMMIT} && pip install .


ENV BUILDSLAVE_NAME diax_wheezy64
ENV BUILDSLAVE_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV BUILDSLAVE_INFO Debian (wheezy) 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
