FROM centos:7

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm 

RUN yum update -y && yum install -y \
    git curl wget mock rpm-build \
    python35u python35u-libs python35u-devel python35u-pip \
    python-pillow-devel \
    && yum groupinstall -y "Development Tools"

RUN ln -s /usr/bin/python3.5 /usr/bin/python3 \
&& ln -s /usr/bin/pip3.5 /usr/bin/pip3

RUN python3 -m pip install "buildbot[bundle]" numpy sphinx Pillow

ENV BUILDSLAVE_NAME diax-centos7-64
ENV BUILDSLAVE_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV BUILDSLAVE_INFO CentOS 7 64-bit
COPY slave-start.sh /root/
CMD /root/slave-start.sh
