from models import Page
from django.http import Http404
from django.shortcuts import render_to_response
from django.conf import settings

# map from ext to (name, mime)
default_extensions = {
    'html' : ('xhtml', 'application/xhtml+xml'),
    'txt' : ('txt', 'text/plain'),
}
default_extension = 'html'

def page(request, url):
    def_ext = getattr(settings, 'PODSTAKANNIK_DEFAULT_EXTENSION', default_extension)
    extensions = getattr(settings, 'PODSTAKANNIK_EXTENSIONS', default_extensions)
    
    # canonicalize url
    url = filter(lambda s: s != '', url.split('/'))
    url = '/' + '/'.join(url)
    
    if '.' in url:
        url, ext = url.split('.', 1)
    else:
        ext = def_ext
    
    if not ext in extensions:
        raise Http404
    
    try:
        p = Page.objects.get(url=url)
    except Page.DoesNotExist:
        raise Http404
    
    extmap = []
    for other_ext in extensions:
        element = {}
        element['current'] = (other_ext == ext)
        element['name'] = extensions[other_ext][0]
        element['url'] = p.get_absolute_url() + '.' + other_ext
        extmap.append(element)
    
    mime = extensions[ext][1]
    
    return render_to_response('podstakannik/page.' + ext, {'page' : p, 'alternates' : extmap}, mimetype=mime)

