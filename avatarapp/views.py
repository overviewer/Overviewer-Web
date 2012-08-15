from __future__ import division

from cStringIO import StringIO

import requests
import Image

from django.http import HttpResponse
from django.core.cache import cache

def get_from_minecraft(player="__default_img__"):
    "Gets an image from minecraft. Returns a PIL Image object. never caches"

    if player == "___default_img__":
        response = requests.get("http://www.minecraft.net/images/char.png")
    else:
        response = requests.get("http://www.minecraft.net/skin/%s.png" % player)
        
        if response.status_code != 200:
            response = requests.get("http://www.minecraft.net/images/char.png")

    try:
        data = StringIO(response.raw.data)
    except IOError:
        # for some reason we get IOError("cannot identify image file") here
        if response.status_code != 200:
            response = requests.get("http://www.minecraft.net/images/char.png")
        data = StringIO(response.raw.data)

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
            (12,8,47,20,4,12), # arm-r
            (4,20,4,20,4,12), # leg-l
            (8,20,7,20,4,12), # leg-r
        ]
    if "A" in skin.mode:
        pastes += [
            (4,0,40,8,8,8), # hat
            ]
    for p in pastes:
        paste(av,skin,*p)
    return av

def create_head_from_skin_with_size(size):
    def skintohead(skin):
        head = skin.crop((8,8,16,16))
        if "A" in skin.mode:
            hat = skin.crop((40,8,48,16))
            head.paste(hat, (0,0), hat)
        return head.resize(size)
    return skintohead

def cachedavmaker(func, name, username):
    image_data = cache.get(username+"|"+name)

    if not image_data:
        skin = get_from_minecraft(username)
        av = func(skin)
        img_buffer = StringIO()
        av.save(img_buffer, format="png")
        image_data = img_buffer.getvalue()
        cache.set(username+"|"+name, image_data, 1800)

    return HttpResponse(image_data, mimetype="image/png")

def getav(request, username):
    return cachedavmaker(create_av_from_skin, "av", username)

def gethead(request, username):
    return cachedavmaker(create_head_from_skin_with_size((16,16)), "head", username)

def getbighead(request, username):
    return cachedavmaker(create_head_from_skin_with_size((64,64)), "bighead", username)
