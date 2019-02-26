import os
import os.path

from ..utils import random_string

ovr = os.path.join(os.path.split(__file__)[0], '..')

DEBUG = True

UPLOADER_PATH = None
UPLOADER_URL = None

BUILDS_URL = None
BUILDBOT_URL = "http://overviewer.org/build/"
BUILDBOT_PUBLIC_URL = BUILDBOT_URL

WTF_CSRF_ENABLED = True
CACHE_TYPE = 'simple'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(ovr, '..', 'overviewer.db'))

# grab confidentials from env
SECRET_KEY = os.environ.get('FLASK_SECRET', random_string(24))
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
