FROM i386/debian:stretch

RUN apt-get update && apt-get -y install \
jq git curl wget devscripts \
python3.5 python3.5-dev python3-numpy python3-pil python3-pip \
&& python3 -m pip install "buildbot[bundle]"

ENV WORKER_NAME diax-stretch-32
ENV WORKER_ADMIN Nicolas Frattaroli <ovdev@fratti.ch>
ENV WORKER_INFO Debian (stretch) 32-bit
COPY worker-start.sh /root/
CMD /root/worker-start.sh
