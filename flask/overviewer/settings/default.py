import os
import os.path
import datetime

from ..utils import random_string

ovr = os.path.join(os.path.split(__file__)[0], '..')

DEBUG = True

UPLOADER_PATH = None
UPLOADER_URL = None

BUILDS_URL = None
BUILDBOT_URL = "https://overviewer.org/build/"
BUILDBOT_PUBLIC_URL = BUILDBOT_URL

WTF_CSRF_ENABLED = True
CACHE_TYPE = 'simple'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(ovr, '..', 'overviewer.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# grab confidentials from env
SECRET_KEY = os.environ.get('FLASK_SECRET', random_string(24))
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
DEBUG_TB_INTERCEPT_REDIRECTS = False

RELEASE_DOWNLOADS = {
  "src": {
    "version": "0.19.10",
    "url": "https://overviewer.org/~pillow/up/013efcfd21/overviewer-0.19.10.tar.gz",
    "date": datetime.datetime.fromisoformat("2023-04-05T16:40:44"),
    "commit": "13c1bddaf65dfaaf6c4c7a396c94db75bed4c089",
    "commiturl": "https://github.com/overviewer/Minecraft-Overviewer/commit/13c1bddaf65dfaaf6c4c7a396c94db75bed4c089"
  },
  "win32": {
    "version": "0.19.9",
    "url": "https://overviewer.org/builds/win32/226/overviewer-0.19.9.zip",
    "url": "https://overviewer.org/~pillow/up/13e16cc46a/overviewer-0.19.9.zip",
    "date": datetime.datetime.fromisoformat("2022-08-14T17:44:36"),
    "commit": "6ffbe0f0beee56288fabce4db8d1838e42bac160",
    "commiturl": "https://github.com/overviewer/Minecraft-Overviewer/commit/6ffbe0f0beee56288fabce4db8d1838e42bac160"
  },
  "win64": {
    "version": "0.19.9",
    "url": "https://overviewer.org/~pillow/up/39502be25c/overviewer-0.19.9-64.zip",
    "date": datetime.datetime.fromisoformat("2022-08-14T17:47:55"),
    "commit": "6ffbe0f0beee56288fabce4db8d1838e42bac160",
    "commiturl": "https://github.com/overviewer/Minecraft-Overviewer/commit/6ffbe0f0beee56288fabce4db8d1838e42bac160"
  },
}
