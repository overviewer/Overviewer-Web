from flask import Blueprint, abort, make_response
from io import BytesIO
import requests
from PIL import Image

from .cache import cache

avatar = Blueprint('avatar', __name__)

def get_from_minecraft(player="__default_img__"):
    "Gets an image from minecraft. Returns a PIL Image object. never caches"

    if player == '__default_img__':
        response = requests.get("https://s3.amazonaws.com/MinecraftSkins/char.png")
    else:
        response = requests.get("https://s3.amazonaws.com/MinecraftSkins/" + player + ".png")
        if response.status_code != 200:
            response = requests.get("https://s3.amazonaws.com/MinecraftSkins/char.png")

    try:
        data = BytesIO(response.content)
    except IOError:
        # for some reason we get IOError("cannot identify image file") here
        if response.status_code != 200:
            response = requests.get("https://s3.amazonaws.com/MinecraftSkins/char.png")
        data = BytesIO(response.content)

    return Image.open(data)

def paste(dst,src,dst_x,dst_y,src_x,src_y,src_w,src_h):
    src = src.crop((src_x,src_y,src_x+src_w,src_y+src_h))
    try:
        dst.paste(src, (dst_x, dst_y), src)
    except ValueError:
        dst.paste(src, (dst_x, dst_y))

def create_av_from_skin(skin):
    av = Image.new("RGBA", (16,32))    
    
    pastes = [
        (4,0,8,8,8,8), # head
        (4,8,20,20,8,12), # body
        (0,8,44,20,4,12), # arm-l
        (12,8,52,20,4,12), # arm-r
        (4,20,4,20,4,12), # leg-l
        (8,20,12,20,4,12), # leg-r
    ]
    if "A" in skin.mode:
        pastes += [
            (4,0,40,8,8,8), # hat
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

@cache.memoize(1800)
def get_avatar(kind, username):
    try:
        skin = get_from_minecraft(username)
        if kind == 'av':
            av = create_av_from_skin(skin)
        elif kind == 'head':
            av = create_head_from_skin_with_size((16, 16), skin)
        elif kind == 'bighead':
            av = create_head_from_skin_with_size((64, 64), skin)
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
@cache.cached(1800)
def default(username):
    return get_avatar('av', username)

@avatar.route('/<username>/body')
@cache.cached(1800)
def body(username):
    return get_avatar('av', username)

@avatar.route('/<username>/head')
@cache.cached(1800)
def head(username):
    return get_avatar('head', username)

@avatar.route('/<username>/bighead')
@cache.cached(1800)
def bighead(username):
    return get_avatar('bighead', username)

