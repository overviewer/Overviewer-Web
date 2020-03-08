FROM centos:8
RUN yum install -y epel-release
RUN yum --exclude=iputils update -y && yum install -y \
    git curl wget mock rpm-build \
    python36 python3-libs python36-devel python3-pip python3-numpy python3-pillow \
    redhat-rpm-config gcc libffi-devel openssl-devel \
    && yum groupinstall -y "Development Tools"
RUN ln -sf /usr/bin/python3.6 /usr/bin/python3 \
    && ln -sf /usr/bin/pip3.6 /usr/bin/pip3

RUN python3 -m pip install "buildbot[bundle]" sphinx

ENV WORKER_NAME diax-centos8-64
ENV WORKER_ADMIN Andrew Chin <andrew@andrewchin.net>
ENV WORKER_INFO CentOS 8 64-bit
COPY worker-start.sh /root/
CMD /root/worker-start.sh
