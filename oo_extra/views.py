from models import Package, PackageModelForm, Build

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import os

@csrf_exempt
def package_hook(request):
    if request.method == 'POST' and 'key' in request.GET and request.GET['key'] == settings.PACKAGE_HOOK_KEY:
        f = PackageModelForm(request.POST)
        f.save()
        return HttpResponse('<pre>Package Posted.</pre>\n')
    
    raise Http404

@csrf_exempt
def update(request):
    if request.method == 'POST' and 'payload' in request.POST and 'key' in request.GET and request.GET['key'] == settings.UPDATE_HOOK_KEY:
        data = request.POST['payload']
        data = json.loads(data)
        ref = data['ref']
        os.system("%s %s" % (settings.UPDATE_HOOK_COMMAND, ref))
        return HttpResponse('<pre>Hook Started</pre>\n')
        
    raise Http404

def latest_build(request, builder='src'):
    pkgs = Build.objects.filter(builder=builder, branch="master")
    try:
        b = pkgs.order_by('-date')[0]
    except IndexError:
        raise Http404
    
    return build(request, b.pk, None)

def build(request, bid, path):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if not user_agent.strip():
        return HttpResponseForbidden("We're sorry, due to abuse we can no longer allow downloads without a user agent. If you are running a script, we ask that you do not unconditionally download a package every hour, as this runs up our bandwidth. Please download the file you need only once, either by adjusting your script or by downloading it manually. Also any automated scripts must properly identify with a user-agent header. For questions, please ask on IRC. Thank you. -The Management")
    
    b = get_object_or_404(Build, pk=bid)
    b.downloads += 1
    b.save()

    response = HttpResponse()
    url = settings.ACCEL_BUILD_URL_PREFIX + b.path
    response['Content-Type'] = ""
    response['X-Accel-Redirect'] = url
    
    return response
