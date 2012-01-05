from models import File, FileForm
from django.core.cache import cache
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required

def upload_progress(request):
    progress_id = None
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')

def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save(commit=False)
            if request.user.is_anonymous():
                m.owner = None
            else:
                m.owner = request.user
            m.save()
        else:
            m = None
    else:
        m = None
        form = FileForm()
    
    return render_to_response('uploader/upload.html', {'file' : m, 'form' : form}, context_instance=RequestContext(request))

def list_uploads(request):
    files = File.objects.all()
    return render_to_response('uploader/list.html', {'files' : files}, context_instance=RequestContext(request))

@permission_required('uploader.delete_file')
def delete(request, file_id):
    f = get_object_or_404(File, id=file_id)
    
    if request.method == 'POST':
        f.delete()
        return HttpResponseRedirect(reverse(list_uploads))

    return render_to_response('uploader/delete.html', {'file' : f}, context_instance=RequestContext(request))
