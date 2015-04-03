FROM debian:wheezy
#FROM luisalejandro/debian-i386

RUN apt-get update && apt-get -y install buildbot-slave

ENV BUILDSLAVE_NAME diax_wheezy64
ENV BUILDSLAVE_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV BUILDSLAVE_INFO Debian (wheezy) 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
