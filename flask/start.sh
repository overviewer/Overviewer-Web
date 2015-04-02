#!/bin/bash

mkdir -p /data/www/static
mkdir -p /data/www/uploads
cp -ruT overviewer/static /data/www/static

python manage.py db upgrade
exec gunicorn -w 4 -b 0.0.0.0:8000 overviewer.app:app
