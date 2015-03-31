from flask import render_template, redirect, flash, url_for, request, make_response
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import re
import functools
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

def render_blog(tmpl, **kwargs):
    monthnames = 'January February March April May June July August September October November December'.split()
    archives = {}
    for p in BlogPost.query.all():
        t = p.timestamp
        y = archives.setdefault(t.year, {})
        m = y.setdefault(t.month, set())
        m.add(t.day)
    archives_nice = []
    years = list(archives.keys())
    years.sort()
    for y in years:
        year = []
        archives_nice.append((str(y), url_for('blog_index_year', year=y), year))
        months = list(archives[y].keys())
        months.sort()
        for m in months:
            month = []
            name = monthnames[m - 1]
            year.append((name, url_for('blog_index_month', year=y, month=m), month))
            days = list(archives[y][m])
            days.sort()
            for d in days:
                month.append((name + ' ' + str(d), url_for('blog_index_day', year=y, month=m, day=d), []))

    return render_template(tmpl, archives=archives_nice, **kwargs)

class PostForm(Form):
    user = StringField('user', validators=[DataRequired()])
    timestamp = DateTimeField('timestamp', validators=[DataRequired()])
    published = BooleanField('published', default=True)
    title = StringField('title', validators=[DataRequired()])
    body = TextAreaField('body')

# decorator to set mime types
def content_type(mime_type, charset=None):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            r = make_response(f(*args, **kwargs))
            r.mimetype = mime_type
            if charset:
                r.charset = charset
            return r
        return inner
    return wrapper

def index_for(query, tmpl='blog_index.html'):
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    posts = query.order_by(BlogPost.timestamp.desc()).paginate(page, per_page=5)
    return render_blog(tmpl, posts=posts.items, page=posts)

@app.route('/blog/')
def blog_index():
    return index_for(BlogPost.query)

@app.route('/blog/feeds/latest/')
@content_type('application/rss+xml')
def blog_rss():
    return index_for(BlogPost.query, tmpl='blog_rss.xml')

@app.route('/blog/<int:year>/')
def blog_index_year(year):
    start = datetime(year=year, month=1, day=1)
    end = datetime(year=year + 1, month=1, day=1)
    return index_for(BlogPost.query.filter(BlogPost.timestamp.between(start, end)))

@app.route('/blog/<int:year>/<int:month>/')
def blog_index_month(year, month):
    start = datetime(year=year, month=month, day=1)
    if month == 12:
        end = datetime(year=year + 1, month=1, day=1)
    else:
        end = datetime(year=year, month=month + 1, day=1)
    return index_for(BlogPost.query.filter(BlogPost.timestamp.between(start, end)))

@app.route('/blog/<int:year>/<int:month>/<int:day>/')
def blog_index_day(year, month, day):
    start = datetime(year=year, month=month, day=day)
    end = start + timedelta(days=1)
    return index_for(BlogPost.query.filter(BlogPost.timestamp.between(start, end)))

def post_route(suffix, **kwargs):
    def wrapper(f):
        @app.route('/blog/<int:year>/<int:month>/<int:day>/<slug>' + suffix, **kwargs)
        @functools.wraps(f)
        def inner(year, month, day, slug):
            start = datetime(year=year, month=month, day=day)
            end = start + timedelta(days=1)
            p = BlogPost.query.filter(BlogPost.timestamp.between(start, end)).filter_by(slug=slug).first_or_404()
            return f(p)
        return inner
    return wrapper

@post_route('/')
def blog_view(post):
    return render_blog('blog_view.html', post=post)

@post_route('/edit', methods=['GET', 'POST'])
def blog_edit(post):
    form = PostForm(user=post.user, timestamp=post.timestamp, published=post.published, title=post.title, body=post.body)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        return redirect(post.url)
    return render_blog('blog_edit.html', form=form)

@post_route('/delete')
def blog_delete(post):
    db.session.delete(post)
    db.session.commit()
    flash('Post `{0}` deleted.'.format(post.title))
    return redirect(url_for('blog_index'))

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
        return redirect(post.url)
    return render_blog('blog_edit.html', form=form)
