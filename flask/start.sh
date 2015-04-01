#!/bin/bash

mkdir -p /data/www/overviewer.org/static
cp -ruT overviewer/static /data/www/overviewer.org/static

python manage.py db upgrade
exec gunicorn -w 4 -b 0.0.0.0:8000 overviewer.app:app
