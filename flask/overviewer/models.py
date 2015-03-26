from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    published = db.Column(db.Boolean)
    title = db.Column(db.String(256))
    slug = db.Column(db.String(128), index=True)
    body = db.Column(db.Text())
