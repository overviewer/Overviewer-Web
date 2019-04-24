from flask import Blueprint, abort, redirect
import requests

from .cache import cache


textures = Blueprint('textures', __name__)


@cache.memoize(1200)
def get_version_manifest():
    M_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = requests.get(M_URL).json()
    assert("latest" in manifest)
    assert("versions" in manifest)
    return manifest


@cache.memoize(3600)
def get_client_manifest(url):
    manifest = requests.get(url).json()
    assert("downloads" in manifest)
    assert("client" in manifest["downloads"])
    return manifest


@textures.route('/<version>')
def get_textures(version):
    ver = version
    m = get_version_manifest()
    c_m_url = ""

    if version == "latest":
        ver = m["latest"]["release"]
    for client in m["versions"]:
        if client["id"] == ver:
            c_m_url = client["url"]
            break
    else:
        return abort(404)
    client_m = get_client_manifest(c_m_url)
    return redirect(client_m["downloads"]["client"]["url"])
