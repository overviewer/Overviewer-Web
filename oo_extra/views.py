from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os

@csrf_exempt
def update(request):
    if request.method == 'POST' and 'payload' in request.POST and 'key' in request.GET and request.GET['key'] == settings.UPDATE_HOOK_KEY:
        data = json.load(request)
        ref = data['ref']
        os.system("%s %s" % (settings.UPDATE_HOOK_COMMAND, ref))
        return HttpResponse('<pre>Hook Started</pre>\n')
        
    raise Http404
