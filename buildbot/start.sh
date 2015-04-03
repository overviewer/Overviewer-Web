#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/master.cfg /root/confidential.py master/
rm -f master/twistd.pid master/twistd.log
buildbot upgrade-master master
exec buildbot start --nodaemon master
