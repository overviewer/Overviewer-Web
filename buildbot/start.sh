#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/master/* master/
rm -f master/twistd.pid master/twistd.log
buildbot upgrade-master master

eval $(gpg-agent --daemon --default-cache-ttl 1000000000 --max-cache-ttl 1000000000 --allow-preset-passphrase)
/usr/lib/gnupg2/gpg-preset-passphrase -P $CODESIGN_PASSPHRASE -c $CODESIGN_KEYGRIP
unset CODESIGN_PASSPHRASE
unset CODESIGN_KEYGRIP

mkdir -p uploads renders

mkdir -p repos/debian/repo/files
cp -r /root/repos/debian repos/
make -C repos/debian/repo

cp -r /root/repos/rpm repos/
mkdir -p repos/rpm/repo/{6,7}/{i386,x86_64}/packages
ln -fs 7 repos/rpm/repo/16
ln -fs 7 repos/rpm/repo/17
ln -fs 7 repos/rpm/repo/18
ln -fs 7 repos/rpm/repo/19
ln -fs 7 repos/rpm/repo/20
ln -fs 7 repos/rpm/repo/21
ln -fs 7 repos/rpm/repo/22
ln -fs 7 repos/rpm/repo/23
ln -fs 7 repos/rpm/repo/24
ln -fs 7 repos/rpm/repo/25
ln -fs 7 repos/rpm/repo/26
ln -fs 7 repos/rpm/repo/27
ln -fs 7 repos/rpm/repo/28
ln -fs 7 repos/rpm/repo/latest
make -C repos/rpm/repo

exec buildbot start --nodaemon master
