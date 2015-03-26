from flask import render_template, redirect, flash, url_for
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
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
    timestamp = DateTimeField('timestamp', validators=[DataRequired()])
    published = BooleanField('published', default=True)
    title = StringField('title', validators=[DataRequired()])
    body = TextAreaField('body')

@app.route('/blog/')
def blog_index():
    entries = BlogPost.query.all()
    return render_template('blog_index.html', entries=entries)

@app.route('/blog/<int:year>/<int:month>/<int:day>/<slug>/')
def blog_view(year, month, day, slug):
    start = datetime(year=year, month=month, day=day)
    end = start + timedelta(days=1)
    
    p = BlogPost.query.filter(BlogPost.timestamp.between(start, end)).filter_by(slug=slug).first_or_404()
    return render_template('blog_view.html', post=p)

@app.route('/blog/create', methods=['GET', 'POST'])
@auth.developer_only
def blog_create():
    form = PostForm(user=auth.user(), timestamp=datetime.now())
    if form.validate_on_submit():
        post = BlogPost()
        form.populate_obj(post)
        post.slug = slugify(post.title)
        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_index'))
    return render_template('blog_create.html', form=form)
