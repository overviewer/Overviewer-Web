FROM debian:stretch

RUN apt-get update && apt-get -y install \
jq git curl wget devscripts \
python3.5 python3-all-dev python3-numpy python3-pil python3-pip \
build-essential libssl-dev libffi-dev

RUN python3 -m pip install "buildbot[bundle]==2.*"

ENV WORKER_NAME diax-stretch-64
ENV WORKER_ADMIN Nicolas Frattaroli <ovdev@fratti.ch>
ENV WORKER_INFO Debian (stretch) 64-bit
COPY worker-start.sh /root/
CMD /root/worker-start.sh
