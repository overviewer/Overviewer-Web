from flask import render_template, redirect, flash, url_for
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime
import re
from unidecode import unidecode

from . import auth
from .app import app
from .models import db, BlogPost

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)

class PostForm(Form):
    user = StringField('user', validators=[DataRequired()])
    published = BooleanField('published', default=True)
    title = StringField('title', validators=[DataRequired()])
    body = StringField('body')

@app.route('/blog/')
def blog_index():
    entries = BlogPost.query.all()
    return render_template('blog_index.html', entries=entries)

@app.route('/blog/create', methods=['GET', 'POST'])
@auth.developer_only
def blog_create():
    form = PostForm(user=auth.user())
    if form.validate_on_submit():
        post = BlogPost()
        form.populate_obj(post)
        post.timestamp = datetime.now()
        post.slug = slugify(post.title)
        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_index'))
    return render_template('blog_create.html', form=form)
