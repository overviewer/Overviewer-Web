from flask import request, url_for, flash, redirect, session, abort
from flask.ext.github import GitHub
import functools
from .app import app

github = GitHub(app)

@app.route('/login')
def login():
    next_url = request.args.get('next') or url_for('index')
    if session.get('logged_in', False):
        return redirect(next_url)
    redirect_uri = url_for('authorize', _external=True)
    redirect_uri += '?next=' + next_url
    return github.authorize(redirect_uri=redirect_uri)

@app.route('/logout')
def logout():
    if session.get('logged_in', False):
        session['logged_in'] = False
        if 'oauth_token' in session:
            del session['oauth_token']
        if 'user' in session:
            del session['user']
        if 'developer' in session:
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
    orgs = [d['login'] for d in github.get('users/' + session['user'] + '/orgs')]
    session['developer'] = 'overviewer' in orgs
    flash('You have logged in as ' + session['user'] + '.')
    return redirect(next_url)

@github.access_token_getter
def token_getter():
    if session.get('logged_in', False):
        return session['oauth_token']

def is_logged_in():
    return session.get('logged_in', False)

def user():
    if is_logged_in():
        return session['user']

def is_developer():
    if is_logged_in():
        return session['developer']
    return False

# use as a decorator!
def developer_only(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        if not is_logged_in():
            abort(401)
        if not is_developer():
            abort(403)
        return f(*args, **kwargs)
    return inner
