import os
import os.path

DEBUG = False

# grab password from env
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

UPLOADER_PATH = "/data/www/uploads/"
UPLOADER_URL = "/_protected/uploads/"

BUILDS_URL = "/_protected/builds/"
BUILDBOT_URL = "http://bbmaster:8010/"

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + POSTGRES_PASSWORD + '@postgres/flask'
