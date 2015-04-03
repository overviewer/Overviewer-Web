import os
import os.path

DEBUG = False

# grab password from env
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

UPLOADER_PATH = "/data/www/uploads/"
UPLOADER_URL = "/_protected/uploads/"

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + POSTGRES_PASSWORD + '@postgres/flask'
