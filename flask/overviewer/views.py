from flask import render_template, request, url_for, flash, redirect, session
from flask.ext.github import GitHub
from .app import app

github = GitHub(app)

@app.route('/login')
def login():
    if session.get('logged_in', False):
        next_url = request.args.get('next') or url_for('index')
        return redirect(next_url)
    return github.authorize()

@app.route('/logout')
def logout():
    if session.get('logged_in', False):
        session['logged_in'] = False
        del session['oauth_token']
        del session['user']
        del session['developer']
        flash('You have logged out.')
    next_url = request.args.get('next') or url_for('index')
    return redirect(next_url)

@app.route('/login/authorize')
@github.authorized_handler
def authorize(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    session['logged_in'] = True
    session['oauth_token'] = oauth_token
    session['user'] = github.get('user')['login']
    orgs = [d['login'] for d in github.get('user/orgs')]
    session['developer'] = 'overviewer' in orgs
    flash('You have logged in as ' + session['user'] + '.')
    return redirect(next_url)

@github.access_token_getter
def token_getter():
    if session.get('logged_in', False):
        return session['oauth_token']

@app.route('/')
def index():
    return render_template('index.html')

# Shortcuts...
def shortcut(paths, destination):
    for path in paths:
        n1 = 'shortcut' + path.replace('/', '_')
        n2 = 'shortcut_path' + path.replace('/', '_')
        app.add_url_rule(path, n1, lambda: redirect(destination))
        app.add_url_rule(path + '/<path:path>', n2, lambda path: redirect(destination + '/' + path))

shortcut(['/wiki'], 'https://github.com/overviewer/Minecraft-Overviewer/wiki')
shortcut(['/issues'], 'https://github.com/overviewer/Minecraft-Overviewer/issues')
shortcut(['/code', '/git'], 'https://github.com/overviewer/Minecraft-Overviewer')
shortcut(['/pulls'], 'https://github.com/overviewer/Minecraft-Overviewer/pulls')
shortcut(['/pull'], 'https://github.com/overviewer/Minecraft-Overviewer/pull')
shortcut(['/doc', '/docs'], 'http://docs.overviewer.org/')
