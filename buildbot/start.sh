#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/{master.cfg,confidential.py,debian.tar} master/
rm -f master/twistd.pid master/twistd.log
mkdir -p uploads
buildbot upgrade-master master
exec buildbot start --nodaemon master
