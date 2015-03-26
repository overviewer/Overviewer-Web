import os
from flask import Flask
from .models import db

app = Flask(__package__)

app.config.from_object('overviewer.settings.confidential')
app.config.from_object('overviewer.settings.default')
if 'OVERVIEWER_SETTINGS' in os.environ:
    app.config.from_envvar('OVERVIEWER_SETTINGS')

db.init_app(app)
