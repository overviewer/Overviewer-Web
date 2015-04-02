import os.path

ovr = os.path.join(os.path.split(__file__)[0], '..')

DEBUG = True

UPLOADER_PATH = None
UPLOADER_URL = None

WTF_CSRF_ENABLED = True
CACHE_TYPE = 'simple'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(ovr, '..', 'overviewer.db'))
