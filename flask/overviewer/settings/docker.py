import os.path

DEBUG = False

conf = os.path.join(os.path.split(__file__)[0], 'confidential.py')
with open(conf) as f:
    s = f.read()
    exec(s)

UPLOADER_PATH = "/data/www/uploads/"
UPLOADER_URL = "/_protected/uploads/"

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + DOCKER_DB_PASSWORD + '@postgres/flask'
