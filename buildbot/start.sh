#!/bin/bash

cd /data/buildbot
if [ ! -d "master" ]; then
    echo "creating master..."
    buildbot create-master master
fi

cp /root/{master.cfg,debian.tar,rpm.tar} master/
rm -f master/twistd.pid master/twistd.log
buildbot upgrade-master master

eval $(gpg-agent --daemon --default-cache-ttl 1000000000 --max-cache-ttl 1000000000 --allow-preset-passphrase)
/usr/lib/gnupg2/gpg-preset-passphrase -P $CODESIGN_PASSPHRASE -c $CODESIGN_KEYGRIP
unset CODESIGN_PASSPHRASE
unset CODESIGN_KEYGRIP

mkdir -p uploads renders

mkdir -p repos/debian/files
cp /root/debian-repo/* repos/debian/
make -C repos/debian/

mkdir -p repos/rpm
cp /root/rpm-repo/* repos/rpm/
mkdir -p repos/rpm/{6,7}/{i386,x86_64}/packages
ln -fs 7 repos/rpm/16
ln -fs 7 repos/rpm/17
ln -fs 7 repos/rpm/18
ln -fs 7 repos/rpm/19
ln -fs 7 repos/rpm/20
ln -fs 7 repos/rpm/21
ln -fs 7 repos/rpm/22
ln -fs 7 repos/rpm/23
ln -fs 7 repos/rpm/24
ln -fs 7 repos/rpm/25
ln -fs 7 repos/rpm/26
ln -fs 7 repos/rpm/27
ln -fs 7 repos/rpm/28
ln -fs 7 repos/rpm/latest
make -C repos/rpm/

exec buildbot start --nodaemon master
