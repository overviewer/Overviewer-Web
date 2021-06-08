FROM centos:7
RUN yum install -y epel-release
RUN yum --exclude=iputils update -y && yum install -y \
    git curl wget mock rpm-build \
    python36 python36-libs python36-devel python36-pip python36-numpy python3-pillow \
    redhat-rpm-config gcc libffi-devel openssl-devel \
    && yum groupinstall -y "Development Tools"
RUN ln -sf /usr/bin/python3.6 /usr/bin/python3 \
    && ln -sf /usr/bin/pip3.6 /usr/bin/pip3

RUN python3 -m pip install -U pip==20.3.4
RUN python3 -m pip install "buildbot[bundle]" sphinx

ENV WORKER_NAME diax-centos7-64
ENV WORKER_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV WORKER_INFO CentOS 7 64-bit
COPY worker-start.sh /root/
CMD /root/worker-start.sh
