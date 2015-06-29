from flask import url_for, current_app, session
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import os.path
import os
import hashlib
from datetime import datetime

db = SQLAlchemy()

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True)
    published = db.Column(db.Boolean, index=True)
    title = db.Column(db.String(256))
    slug = db.Column(db.String(128), index=True, unique=True)
    body = db.Column(db.Text())

    def get_url(self, **kwargs):
        t = self.timestamp
        return url_for('blog_view', year=t.year, month=t.month, day=t.day, slug=self.slug, **kwargs)
    
    @property
    def url(self):
        return self.get_url()

    @property
    def user_url(self):
        return 'https://github.com/' + self.user

def copy_file_and_hash(src, dest=None, bufsize=16384, hasher=hashlib.md5):
    m = hasher()
    size = 0
    while True:
        b = src.read(bufsize)
        if not b:
            break
        size += len(b)
        m.update(b)
        if dest:
            dest.write(b)
    return m.hexdigest(), size

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128), nullable=True)
    timestamp = db.Column(db.DateTime, index=True)
    name = db.Column(db.String(1024))
    path = db.Column(db.String(1024))
    md5 = db.Column(db.String(32))
    size = db.Column(db.Integer)

    @classmethod
    def upload(cls, f):
        dest = current_app.config.get('UPLOADER_PATH')
        now = datetime.now()
        
        name, ext = os.path.splitext(secure_filename(f.filename))
        path = name + now.strftime('.%Y-%m-%d.%H-%M-%S') + ext
        if dest:
            fullpath = os.path.join(dest, path)
            with open(fullpath, 'wb') as out:
                md5, size = copy_file_and_hash(f.stream, out)
        else:
            md5, size = copy_file_and_hash(f.stream)

        user = None
        if session.get('logged_in', False):
            user = session['user']
        m = cls(user=user, timestamp=now, path=path, md5=md5, size=size, name=f.filename)

        db.session.add(m)
        db.session.commit()
        return m

    @property
    def nice_size(self):
        oom = ['bytes', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        size = self.size
        for i, mag in enumerate(oom):
            if int(size / 1024) == 0:
                return "{0} {1}".format(round(size), mag)
            size /= 1024
        return "(unknown; > 1024 YiB)"

    def delete(self):
        dest = current_app.config.get('UPLOADER_PATH')
        if dest:
            fullpath = os.path.join(dest, self.path)
            if os.path.exists(fullpath):
                os.unlink(fullpath)
        db.session.delete(self)
        db.session.commit()

    @property
    def url(self):
        return url_for('uploader.download', id=self.id, name=self.name)

    @property
    def internal_url(self):
        base = current_app.config.get('UPLOADER_URL')
        if not base:
            base = '/PREFIX/'
        return base + self.path
