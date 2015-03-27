from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from overviewer.app import app
from overviewer.models import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def load_blog(path):
    from overviewer.models import BlogPost
    import pytoml
    with open(path) as f:
        dat = pytoml.load(f)
    for p in dat['posts']:
        db.session.add(BlogPost(**p))
        print('adding', p['title'])
    db.session.commit()

if __name__ == '__main__':
    manager.run()
