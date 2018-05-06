from flask import render_template, current_app, make_response, abort
from werkzeug.exceptions import HTTPException
import requests
import json
from datetime import datetime

from .app import app
from .cache import cache
from .content_type import content_type

JSON_FTIME = "%a, %d %b %Y %H:%M:%S +0000"

def getbb(path, *args, **kwargs):
    try:
        base = current_app.config.get('BUILDBOT_URL')
        return requests.get(base + path.format(*args, **kwargs)).json()
    except Exception:
        return abort(404)

def getbuild(builder, buildnum):
    try:
        d = getbb("json/builders/{0}/builds/{1}", builder, buildnum)
        r = dict(
            properties = {k: v for k, v, _ in d['properties']},
            name = d['builderName'],
            reason = d['reason'],
            slave = d['slave'],
            eta = d.get('eta'),
        )
    
        r['version'] = r['properties']['version']
        r['number'] = r['properties']['buildnumber']
        r['commit'] = r['properties']['got_revision']
        r['commiturl'] = r['properties']['repository'] + '/commit/' + r['properties']['got_revision']
        r['statusurl'] = current_app.config.get('BUILDBOT_PUBLIC_URL') + 'builders/' + r['name'] + '/builds/' + str(r['number'])
        r['project'] = r['properties'].get('project')
        r['release_build'] = r['properties'].get('release_build', False)
        
        start, end = d.get('times', (None, None))
        if end:
            if d.get('results', 0):
                r['status'] = 'failed'
            else:
                r['status'] = 'finished'
        else:
            r['status'] = 'running'
    
        r['date'] = datetime.utcfromtimestamp(start)
    
        uploads = [x for x in d['steps'] if x['name'] == 'upload']
        if uploads and uploads[0]['urls']:
            r['file'], = uploads[0]['urls'].keys()
            r['url'], = uploads[0]['urls'].values()
            r['basename'] = r['url'].rsplit('/', 1)[-1]
    
        return r
    except KeyError:
        return abort(404)

# grabs all release builds until the first success
# unless it has to go through `limit` builds first
# discards failed release builds
@cache.memoize(1800)
def getreleases(builder, allow_running=True, limit=100):
    # special case for windows -- hardcode the results
    if builder == 'win64':
        return [{"status": "finished",
                 "url": "http://static.overviewer.org/builds/master/1124/overviewer-win64-0.12.254.zip",
                 "basename": "overviewer-win64-0.12.254.zip",
                 "version": "0.12.254",
                 "date": datetime.strptime("2018-05-06", "%Y-%m-%d"),
                 "commit": "b9be8f8ffdc5f5d86b39a689c52518338d18b8ab",
                 "commiturl": "https://github.com/overviewer/Minecraft-Overviewer/commit/b9be8f8ffdc5f5d86b39a689c52518338d18b8ab",
                 }]
    if builder == 'win32':
        return [{"status": "finished",
                 "url": "http://static.overviewer.org/builds/master/1124/overviewer-win32-0.12.254.zip",
                 "basename": "overviewer-win32-0.12.254.zip",
                 "version": "0.12.254",
                 "date": datetime.strptime("2018-05-06", "%Y-%m-%d"),
                 "commit": "b9be8f8ffdc5f5d86b39a689c52518338d18b8ab",
                 "commiturl": "https://github.com/overviewer/Minecraft-Overviewer/commit/b9be8f8ffdc5f5d86b39a689c52518338d18b8ab",
                 }]
    releases = []
    for i in range(-1, -limit, -1):
        try:
            b = getbuild(builder, i)
        except HTTPException:
            break
        if not b['release_build']:
            continue
        
        if b['status'] != 'failed' and (allow_running or b['status'] != 'running'):
            releases.append(b)
        if b['status'] == 'finished':
            break
    return releases

def get_all_releases(builders, allow_running=True):
    return {builder: getreleases(builder, allow_running) for builder in builders}

def collate_releases(builds, keyer=lambda x: x['version']):
    collated = {}
    for builder, releases in builds.items():
        for b in releases:
            v = collated.setdefault(keyer(b), {})
            x = v.setdefault(builder, [])
            x.append(b)
    return collated

def sort_versions(l):
    def split_ver(v):
        return [int(x) for x in v.split('.')]
    l.sort(key=split_ver)

def choose_releases(builders, allow_running=True):
    rs = get_all_releases(builders, allow_running)
    collated = collate_releases(rs)
    if not collated:
        return ({"version": "unknown", "commit": "unknown", "date": datetime.now()}, {})

    most = max([len(l) for l in collated.values()])
    versions = []
    for v, xs in collated.items():
        if len(xs) >= most:
            versions.append(v)

    sort_versions(versions)
    version = versions[-1]
    best = collated[version]
    example = list(best.values())[0][0]

    choices = {}
    for builder in builders:
        try:
            choices[builder] = best[builder][0]
        except (KeyError, IndexError):
            try:
                finished = [x for x in rs[builder] if x['status'] == 'finished']
                choices[builder] = finished[0]
            except IndexError:
                pass
    return (example, choices)

DOWNLOADS_TREE = [
    ('Source', [('', 'src')]),
    ('Windows', [
        ('32-bit', 'win32'),
        ('64-bit', 'win64'),
    ]),
    ('Debian/Ubuntu', [
        ('32-bit', 'deb32'),
        ('64-bit', 'deb64'),
    ]),
    ('Fedora 16+', [
        ('32-bit', 'fc19-32'),
        ('64-bit', 'fc19-64'),
    ]),
    ('RedHat EL5', [
        ('32-bit', 'el5-32'),
        ('64-bit', 'el5-64'),
    ]),
    ('RedHat EL6', [
        ('32-bit', 'el6-32'),
        ('64-bit', 'el6-64'),
    ]),
]

DOWNLOADS_BUILDERS = []
for _, bs in DOWNLOADS_TREE:
    for _, b in bs:
        DOWNLOADS_BUILDERS.append(b)

@app.route('/downloads.json')
@content_type('application/json')
def downloads_json():
    _, choices = choose_releases(DOWNLOADS_BUILDERS, allow_running=False)
    def simplify(b):
        return dict(
            version = b['version'],
            url = b['url'],
            date = b['date'].strftime(JSON_FTIME),
            commit = b['commit'],
            commiturl = b['commiturl'],
        )
    return json.dumps({k: simplify(v) for k, v in choices.items()}, indent=2)

@app.route('/downloads')
def downloads():
    example, choices = choose_releases(DOWNLOADS_BUILDERS, allow_running=True)
    return render_template('downloads.html', example=example, builds=choices, tree=DOWNLOADS_TREE)

def info_intern(b):
    b['date'] = b['date'].strftime(JSON_FTIME)
    return json.dumps(b, indent=2)

def download_intern(b):
    if b['status'] == 'finished' and 'file' in b:
        response = make_response('')
        response.headers['Content-Type'] = ''
        base = current_app.config.get('BUILDS_URL')
        if not base:
            base = '/PREFIX/'
        response.headers['X-Accel-Redirect'] = base + b['file']
        return response
    return abort(404)

def get_latest(builder):
    bs = getreleases(builder, allow_running=False)
    if not bs:
        return abort(404)
    return bs[0]

@app.route('/builds/overviewer-latest.<ext>.json')
@content_type('application/json')
def latest_src_info(ext):
    return info_intern(get_latest('src'))

@app.route('/builds/overviewer-latest.<ext>')
def latest_src(ext):
    return download_intern(get_latest('src'))

@app.route('/builds/overviewer-latest-<builder>.<ext>.json')
@content_type('application/json')
def latest_info(builder, ext):
    return info_intern(get_latest(builder))

@app.route('/builds/overviewer-latest-<builder>.<ext>')
def latest(builder, ext):
    return download_intern(get_latest(builder))

@app.route('/builds/<builder>/<int:buildnum>/<slug>.json')
@content_type('application/json')
def info(builder, buildnum, slug):
    return info_intern(getbuild(builder, buildnum))

@app.route('/builds/<builder>/<int:buildnum>/<slug>')
def download(builder, buildnum, slug):
    return download_intern(getbuild(builder, buildnum))
