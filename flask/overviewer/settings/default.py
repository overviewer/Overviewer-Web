import os.path

ovr = os.path.join(os.path.split(__file__)[0], '..')

DEBUG = True

WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(ovr, '..', 'overviewer.db'))
