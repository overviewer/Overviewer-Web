FROM fedora:21

# Probably good to make this match what's in the master Dockerfile
ENV BUILDBOT_COMMIT dd6632af2

RUN yum install -y git curl wget python-devel mock rpm-build numpy && yum groupinstall -y "Development Tools" && curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python2

RUN cd /root && git clone https://github.com/buildbot/buildbot.git
RUN cd /root/buildbot && git checkout ${BUILDBOT_COMMIT} && cd /root/buildbot/slave && pip install .


ENV BUILDSLAVE_NAME diax-fc21-64
ENV BUILDSLAVE_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV BUILDSLAVE_INFO Fedora Core 21 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
