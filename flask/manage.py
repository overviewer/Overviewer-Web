from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from overviewer.app import app
from overviewer.models import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
