from flask import render_template, redirect
from .app import app
from .models import BlogPost

from .auth import *
from .blog import *

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).limit(3).all()
    return render_template('index.html', posts=posts)

# Shortcuts...
def shortcut(paths, destination):
    for path in paths:
        n1 = 'shortcut' + path.replace('/', '_')
        n2 = 'shortcut_path' + path.replace('/', '_')
        app.add_url_rule(path, n1, lambda: redirect(destination))
        app.add_url_rule(path + '/<path:path>', n2, lambda path: redirect(destination + '/' + path))

# shortcuts to github!
shortcut(['/wiki'], 'https://github.com/overviewer/Minecraft-Overviewer/wiki')
shortcut(['/issues'], 'https://github.com/overviewer/Minecraft-Overviewer/issues')
shortcut(['/code', '/git'], 'https://github.com/overviewer/Minecraft-Overviewer')
shortcut(['/pulls'], 'https://github.com/overviewer/Minecraft-Overviewer/pulls')
shortcut(['/pull'], 'https://github.com/overviewer/Minecraft-Overviewer/pull')

# shortcuts to RTD
shortcut(['/doc', '/docs'], 'http://docs.overviewer.org/')
shortcut(['/debian/info'], 'http://docs.overviewer.org/en/latest/installing/#debian-ubuntu')
shortcut(['/rpms/info'], 'http://docs.overviewer.org/en/latest/installing/#centos-rhel-fedora')
