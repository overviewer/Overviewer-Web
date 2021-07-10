from flask import Blueprint, abort, make_response
from io import BytesIO
import requests
import json
import base64
from PIL import Image

from .cache import cache

avatar = Blueprint('avatar', __name__)

@cache.memoize(3600)
def get_uuid(username):
    response = requests.get("https://api.mojang.com/users/profiles/minecraft/{}".format(username))
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8', 'ignore'))["id"]

@cache.memoize(3600)
def get_skin_data(uuid):
    skinData = {
        "url": "",
        "slim": False
    }
    response = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid))
    if response.status_code == 200:
        profile = json.loads(response.content.decode('utf-8', 'ignore'))
        properties = profile["properties"]
        textures = next(filter(lambda obj: obj["name"] == "textures", properties), None)
        if textures is None:
            return ""
        textures = base64.b64decode(textures["value"])
        textures = json.loads(textures.decode('utf-8', 'ignore'))
        if "SKIN" in textures["textures"]:
            skinData["url"] = textures["textures"]["SKIN"]["url"]
        else:
            return skinData
        if "metadata" in textures["textures"]["SKIN"]:
            skinData["slim"] = (textures["textures"]["SKIN"]["metadata"]["model"] == "slim")
        return skinData

def get_from_minecraft(player="__default_img__"):
    """Gets an image from minecraft. Returns a PIL Image object. Never caches,
    but the skin URL and the UUID resolution may be cached."""

    skinURL = "http://assets.mojang.com/SkinTemplates/steve.png"
    skinSlim = False
    uuid = get_uuid(player)
    if uuid:
        skinData = get_skin_data(uuid)
        skinURL = skinData["url"] or skinURL
        skinSlim = skinData["slim"] or False
    response = requests.get(skinURL)
    data = BytesIO(response.content)
    return {
        "skin": Image.open(data),
        "slim": skinSlim
    }

def paste(dst,src,dst_x,dst_y,src_x,src_y,src_w,src_h):
    src = src.crop((src_x,src_y,src_x+src_w,src_y+src_h))
    try:
        dst.paste(src, (dst_x, dst_y), src)
    except ValueError:
        dst.paste(src, (dst_x, dst_y))

def create_av_from_skin(skin, slim):
    av = Image.new("RGBA", (16,32))
    width, height = skin.size
    isLegacySkin = (height <= 32)

    # Pre Minecraft 1.8 "legacy" skin:
    #  - head
    #  - hat
    #  - body
    #  - shared leg texture for both left and right leg
    #  - shared arm texture for both left and right arm
    #  - no armor layer except head/hat
    if isLegacySkin:
        # body layer
        pastes = [
            (4, 0, 8, 8, 8, 8), # head
            (4, 8, 20, 20, 8, 12), # body
            (0, 8, 44, 20, 4, 12), # right arm
            (12, 8, 44, 20, 4, 12), # left arm
            (4, 20, 4, 20, 4, 12), # right leg
            (8, 20, 4, 20, 4, 12), # left leg
        ]
        # armor layer
        if "A" in skin.mode:
            pastes += [
                (4, 0, 40, 8, 8, 8) # head
            ]

    # Post Minecraft 1.8 "modern" skin with slim player model:
    #  - head
    #  - head armor
    #  - body
    #  - body armor
    #  - right leg
    #  - right leg armor
    #  - left arm (3px wide)
    #  - left arm armor (3px wide)
    #  - right arm (3px wide)
    #  - right arm armor (3px wide)
    elif slim:
        pastes = [
            # body layer
            (3, 0, 8, 8, 8, 8), # head
            (3, 8, 20, 20, 8, 12), # body
            (0, 8, 44, 20, 3, 12), # right arm
            (11, 8, 36, 52, 3, 12), # left arm
            (3, 20, 4, 20, 4, 12), # right leg
            (7, 20, 20, 52, 4, 12), # left leg
        ]
        # armor layer
        if "A" in skin.mode:
            pastes += [
                (3, 0, 40, 8, 8, 8), # head
                (3, 8, 20, 36, 8, 12), # body
                (0, 8, 44, 36, 3, 12), # right arm
                (11, 8, 52, 52, 3, 12), # left arm
                (3, 20, 4, 36, 4, 12), # right leg
                (7, 20, 4, 52, 4, 12), # left lag
            ]

    # Post Minecraft 1.8 "modern" skin with normal player model:
    #  - head
    #  - head armor
    #  - body
    #  - body armor
    #  - right leg
    #  - right leg armor
    #  - left arm (4px wide)
    #  - left arm armor (4px wide)
    #  - right arm (4px wide)
    #  - right arm armor (4px wide)
    else:
        pastes = [
            # body layer
            (4, 0, 8, 8, 8, 8), # head
            (4, 8, 20, 20, 8, 12), # body
            (0, 8, 44, 20, 4, 12), # right arm
            (12, 8, 36, 52, 4, 12), # left arm
            (4, 20, 4, 20, 4, 12), # right leg
            (8, 20, 20, 52, 4, 12), # left leg
        ]
        # armor layer
        if "A" in skin.mode:
            pastes += [
                (4, 0, 40, 8, 8, 8), # head
                (4, 8, 20, 36, 8, 12), # body
                (0, 8, 44, 36, 4, 12), # right arm
                (12, 8, 52, 52, 4, 12), # left arm
                (4, 20, 4, 36, 4, 12), # right leg
                (8, 20, 4, 52, 4, 12), # left leg
            ]

    for p in pastes:
        paste(av,skin,*p)
    return av

def create_head_from_skin_with_size(size, skin):
    head = skin.crop((8,8,16,16))
    if "A" in skin.mode:
        hat = skin.crop((40,8,48,16))
        head.paste(hat, (0,0), hat)
    return head.resize(size)

@cache.memoize(86400)
def get_avatar(kind, username):
    try:
        skinData = get_from_minecraft(username)
        if kind == 'av':
            av = create_av_from_skin(skinData["skin"], skinData["slim"])
        elif kind == 'head':
            av = create_head_from_skin_with_size((16, 16), skinData["skin"])
        elif kind == 'bighead':
            av = create_head_from_skin_with_size((64, 64), skinData["skin"])
        else:
            raise NotImplementedError

        img_buffer = BytesIO()
        av.save(img_buffer, format='png')
        image_data = img_buffer.getvalue()

        r = make_response(image_data)
        r.mimetype = 'image/png'
        return r
    except Exception:
        raise
        abort(503)

@avatar.route('/<username>/')
@avatar.route('/<username>')
@cache.cached(86400)
def default(username):
    return get_avatar('av', username)

@avatar.route('/<username>/body')
@cache.cached(86400)
def body(username):
    return get_avatar('av', username)

@avatar.route('/<username>/head')
@cache.cached(86400)
def head(username):
    return get_avatar('head', username)

@avatar.route('/<username>/bighead')
@cache.cached(86400)
def bighead(username):
    return get_avatar('bighead', username)
