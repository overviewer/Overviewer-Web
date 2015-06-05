from flask import render_template, current_app, make_response, abort
import requests

from .app import app

def getbb(path, *args, **kwargs):
    base = current_app.config.get('BUILDBOT_URL')
    return requests.get(base + path.format(*args, **kwargs)).json()

def getbuild(builder, buildnum):
    d = getbb("json/builders/{0}/builds/{1}", builder, buildnum)
    r = dict(
        properties = {k: v for k, v, _ in d['properties']},
        name = d['builderName'],
        reason = d['reason'],
        slave = d['slave'],
        successful = 'successful' in d['text'],
    )

    uploads = [x for x in d['steps'] if x['name'] == 'upload']
    if uploads and uploads[0]['urls']:
        r['file'], = uploads[0]['urls'].keys()

    return r

@app.route('/builds/<builder>/<int:buildnum>/<slug>')
def download(builder, buildnum, slug):
    b = getbuild(builder, buildnum)
    if b['successful'] and 'file' in b:
        response = make_response('')
        response.headers['Content-Type'] = ''
        base = current_app.config.get('BUILDS_URL')
        if not base:
            base = '/PREFIX/'
        response.headers['X-Accel-Redirect'] = base + b['file']
        return response
    return abort(404)
