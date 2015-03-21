#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/master.cfg master/master.cfg
rm -f master/twistd.pid
exec buildbot start --nodaemon master
