#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/{master.cfg,debian.tar} master/
rm -f master/twistd.pid master/twistd.log
mkdir -p uploads
buildbot upgrade-master master

eval $(gpg-agent --daemon --default-cache-ttl 1000000000 --max-cache-ttl 1000000000 --allow-preset-passphrase)
/usr/lib/gnupg2/gpg-preset-passphrase -P $CODESIGN_PASSPHRASE -c $CODESIGN_KEYGRIP
unset CODESIGN_PASSPHRASE
unset CODESIGN_KEYGRIP

exec buildbot start --nodaemon master
