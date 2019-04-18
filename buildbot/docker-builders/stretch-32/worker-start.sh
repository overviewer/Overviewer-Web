#!/bin/bash

cd /root/
if [ ! -d "worker" ]; then
    echo "creating worker..."
    buildbot-worker create-worker --umask=0o22 --no-logrotate worker bbmaster:9989 $WORKER_NAME $(python3 -c "import hmac, hashlib; print(hmac.new(bytes('$BUILDBOT_SECRET', 'utf-8'), bytes('$WORKER_NAME', 'utf-8'), hashlib.sha512).hexdigest())")
    echo $WORKER_ADMIN > worker/info/admin
    echo $WORKER_INFO > worker/info/host
    uname -a >> worker/info/host
fi

rm -f worker/twistd.pid worker/twistd.log

# run in a clean env, don't leak secrets
exec env -i -- /bin/bash -c "source /etc/profile; export HOME=`pwd`; exec buildbot-worker start --nodaemon worker"
