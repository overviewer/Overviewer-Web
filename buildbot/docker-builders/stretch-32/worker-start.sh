#!/bin/bash

cd /root/
if [ ! -d "worker" ]; then
    echo "creating worker..."
    buildbot-worker create-worker --umask=022 --no-logrotate worker bbmaster:9989 $WORKER_NAME $(python2 -c "import hmac, hashlib; print hmac.new('$BUILDBOT_SECRET', '$WORKER_NAME', hashlib.sha512).hexdigest()")
    echo $WORKER_ADMIN > worker/info/admin
    echo $WORKER_INFO > worker/info/host
    uname -a >> worker/info/host
fi

rm -f worker/twistd.pid worker/twistd.log

# run in a clean env, don't leak secrets
exec env -i -- /bin/bash -c "source /etc/profile; export HOME=`pwd`; exec buildbot-worker start --nodaemon worker"
