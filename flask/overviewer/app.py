import os
from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__package__)

app.config.from_object('overviewer.settings.confidential')
app.config.from_object('overviewer.settings.default')
if 'OVERVIEWER_SETTINGS' in os.environ:
    app.config.from_envvar('OVERVIEWER_SETTINGS')

from .models import db
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
