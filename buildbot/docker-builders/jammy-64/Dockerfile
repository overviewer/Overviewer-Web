FROM ubuntu:jammy

RUN apt-get update && apt-get -y install \
jq git curl wget devscripts \
python3 python3-all-dev python3-numpy python3-pil python3-pip \
build-essential libssl-dev libffi-dev dh-python debhelper

RUN python3 -m pip install -U pip
RUN python3 -m pip install "buildbot[bundle]==2.*"

ENV WORKER_NAME diax-jammy-64
ENV WORKER_ADMIN Nicolas Frattaroli <ovdev@fratti.ch>
ENV WORKER_INFO Ubuntu (jammy) 64-bit
COPY worker-start.sh /root/
CMD /root/worker-start.sh
