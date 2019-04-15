FROM debian:stretch

RUN apt-get update && apt-get -y install \
jq git curl wget devscripts \
python3.5 python3.5-dev python3-numpy python3-pil python3-pip \
&& python3 -m pip install "buildbot[bundle]"

ENV BUILDSLAVE_NAME diax-stretch-64
ENV BUILDSLAVE_ADMIN Nicolas Frattaroli <ovdev@fratti.ch>
ENV BUILDSLAVE_INFO Debian (stretch) 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
