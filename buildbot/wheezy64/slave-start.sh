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

exec buildslave start --nodaemon slave
