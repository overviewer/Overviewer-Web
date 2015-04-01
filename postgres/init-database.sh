gosu postgres postgres --single -jE <<EOF
CREATE DATABASE "flask" WITH OWNER="postgres" TEMPLATE=template0 ENCODING='UTF8';
EOF

gosu postgres postgres --single -jE <<EOF
CREATE DATABASE "bbmaster" WITH OWNER="postgres" TEMPLATE=template0 ENCODING='UTF8';
EOF
