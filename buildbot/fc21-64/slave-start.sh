#!/bin/bash

cd /root/
if [ ! -d "slave" ]; then
    echo "creating slave..."
    buildslave create-slave --umask=022 --no-logrotate slave bbmaster:9989 $BUILDSLAVE_NAME $(python2 -c "import hmac, hashlib; print hmac.new('$BUILDBOT_SECRET', '$BUILDSLAVE_NAME', hashlib.sha512).hexdigest()")
    echo $BUILDSLAVE_ADMIN > slave/info/admin
    echo $BUILDSLAVE_INFO > slave/info/host
    uname -a >> slave/info/host
fi

rm -f slave/twistd.pid slave/twistd.log

# make sure /sys is rw (I HAVE NO IDEA but it helps rpm builders)
mount -o remount,rw /sys

# run in a clean env, don't leak secrets
exec env -i -- /bin/bash -c "source /etc/profile; export HOME=`pwd`; exec buildslave start --nodaemon slave"
