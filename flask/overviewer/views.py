from flask import render_template, redirect
from .app import app
from .models import BlogPost

from .auth import *
from .blog import *
from .avatar import *
from .uploader import *

app.register_blueprint(avatar, url_prefix='/avatar')
app.register_blueprint(uploader, url_prefix='/uploader')

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).limit(3).all()
    return render_template('index.html', posts=posts)

# static pages...
def static(path, tmpl=None):
    name = 'static' + path.replace('/', '_').replace('.', '_')
    if tmpl is None:
        tmpl = name + '.html'
    app.add_url_rule(path, name, lambda: render_template(tmpl))

static('/donate')
static('/irc/')
static('/irc/bot')
static('/irc/rules')

# Shortcuts...
def shortcut(paths, destination):
    for path in paths:
        n1 = 'shortcut' + path.replace('/', '_').replace('.', '_')
        n2 = 'shortcut_path' + path.replace('/', '_').replace('.', '_')
        app.add_url_rule(path, n1, lambda: redirect(destination))
        app.add_url_rule(path + '/<path:path>', n2, lambda path: redirect(destination + '/' + path))

# shortcuts to ourselves
shortcut(['/upload', '/uploads'], '/uploader')

# shortcuts to github!
shortcut(['/wiki'], 'https://github.com/overviewer/Minecraft-Overviewer/wiki')
shortcut(['/issues'], 'https://github.com/overviewer/Minecraft-Overviewer/issues')
shortcut(['/code', '/git'], 'https://github.com/overviewer/Minecraft-Overviewer')
shortcut(['/pulls'], 'https://github.com/overviewer/Minecraft-Overviewer/pulls')
shortcut(['/pull'], 'https://github.com/overviewer/Minecraft-Overviewer/pull')
shortcut(['/humans.txt'], 'https://raw.githubusercontent.com/overviewer/Minecraft-Overviewer/master/CONTRIBUTORS.rst')

# shortcuts to RTD
shortcut(['/doc', '/docs'], 'http://docs.overviewer.org/')
shortcut(['/debian/info'], 'http://docs.overviewer.org/en/latest/installing/#debian-ubuntu')
shortcut(['/rpms/info'], 'http://docs.overviewer.org/en/latest/installing/#centos-rhel-fedora')
