from models import Page, PageAddForm, PageEditForm, PageMoveForm, File, FileForm
from reversion.models import Version
import reversion
from mptt.forms import MoveNodeForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.conf import settings

# map from ext to (name, mime)
default_extensions = {
    'html' : ('xhtml', 'application/xhtml+xml'),
    'txt' : ('txt', 'text/plain'),
}
default_extension = 'html'

def canonicalize_url(url, def_ext=''):
    url = filter(lambda s: s != '', url.split('/'))
    url = '/' + '/'.join(url)
    
    if '.' in url:
        url, ext = url.split('.', 1)
    else:
        ext = def_ext
    
    # special case
    if url == '/root':
        url = '/'
    
    return url, ext

def page(request, url):
    def_ext = getattr(settings, 'PODSTAKANNIK_DEFAULT_EXTENSION', default_extension)
    extensions = getattr(settings, 'PODSTAKANNIK_EXTENSIONS', default_extensions)
    url, ext = canonicalize_url(url, def_ext)
    if not ext in extensions:
        raise Http404
    
    if 'revision' in request.GET:
        try:
            revision = int(request.GET['revision'])
        except:
            raise Http404
        
        ver = get_object_or_404(Version, revision=revision)
        p = ver.get_object_version().object
    else:
        p = get_object_or_404(Page, url=url)
    
    extmap = []
    for other_ext in extensions:
        element = {}
        element['current'] = (other_ext == ext)
        element['name'] = extensions[other_ext][0]
        element['url'] = p.get_absolute_url() + '.' + other_ext
        extmap.append(element)
    
    mime = extensions[ext][1]
    
    return render_to_response('podstakannik/page.' + ext, {'page' : p, 'alternates' : extmap}, mimetype=mime, context_instance=RequestContext(request))

@reversion.revision.create_on_success
def edit_or_add(request, url, add=False):
    url, _ = canonicalize_url(url)
    p = get_object_or_404(Page, url=url)
    verb = 'add' if add else 'edit'
    preview = None
    
    if request.method == 'POST':
        if add:
            form = PageAddForm(request.POST)
        else:
            form = PageEditForm(request.POST, instance=p)
        if form.is_valid():
            if 'preview' in request.POST:
                preview = form.cleaned_data['body']
            else:
                # save the valid data
                reversion.revision.comment = 'Initial version.' if add else form.cleaned_data['message']
                reversion.revision.user = request.user
                p = form.save()
                return HttpResponseRedirect(p.get_absolute_url())
    else:
        if add:
            form = PageAddForm(initial={'license' : p.license.id, 'parent' : p.id})
        else:
            form = PageEditForm(instance=p)
    
    return render_to_response('podstakannik/edit.html', {'form' : form, 'page' : p, 'preview' : preview, 'verb' : verb}, context_instance=RequestContext(request))

@permission_required('podstakannik.change_page')
def edit(request, url):
    return edit_or_add(request, url, False)

@permission_required('podstakannik.add_page')
def add(request, url):
    return edit_or_add(request, url, True)

@permission_required('podstakannik.add_page')
@permission_required('podstakannik.delete_page')
@reversion.revision.create_on_success
def move(request, url):
    url, _ = canonicalize_url(url)
    p = get_object_or_404(Page, url=url)
    
    if request.method == 'POST':
        node_form = MoveNodeForm(p, request.POST)
        if node_form.is_valid():
            old_url = p.url
            p = node_form.save()
            url_form = PageMoveForm(request.POST, instance=p)
            if url_form.is_valid():
                p = url_form.save()
                new_url = p.calculated_url
                if old_url != new_url:
                    message = "Moved from '%s' to '%s'." % (old_url, p.calculated_url)
                else:
                    message = "Moved without changing url."
                reversion.revision.comment = message
                reversion.revision.user = request.user
                
                return HttpResponseRedirect(p.get_absolute_url())
        else:
            url_form = PageMoveForm(request.POST, instance=p)
    else:
        url_form = PageMoveForm(instance=p)
        node_form = MoveNodeForm(p)
    
    return render_to_response('podstakannik/move.html', {'url_form' : url_form, 'node_form' : node_form, 'page' : p}, context_instance=RequestContext(request))

@permission_required('podstakannik.delete_page')
def delete(request, url):
    url, _ = canonicalize_url(url)
    p = get_object_or_404(Page, url=url)
    
    if request.method == 'POST':
        parent = p.parent
        p.delete()
        if parent:
            return HttpResponseRedirect(parent.get_absolute_url())
        return HttpResponseRedirect('/')

    return render_to_response('podstakannik/delete.html', {'page' : p}, context_instance=RequestContext(request))

def history(request, url):
    url, _ = canonicalize_url(url)
    p = get_object_or_404(Page, url=url)
    
    history = Version.objects.get_for_object(p).reverse()
    
    return render_to_response('podstakannik/history.html', {'page' : p, 'history' : history}, context_instance=RequestContext(request))

###################

def list_files(request, url):
    url, _ = canonicalize_url(url)
    p = get_object_or_404(Page, url=url)
    
    if request.method == 'POST' and request.user.has_perm('podstakannik.add_file'):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save(commit=False)
            m.owner = request.user
            m.parent = p
            m.save()
            return HttpResponseRedirect(p.files_url)
    else:
        form = FileForm()
    
    files = p.file_set.all()
    return render_to_response('podstakannik/list_files.html', {'page' : p, 'files' : files, 'form' : form}, context_instance=RequestContext(request))

def file(request, url, name):
    url, _ = canonicalize_url(url)
    f = get_object_or_404(File, name=name, parent__url=url)
    
    return HttpResponseRedirect(f.file.url)

@permission_required('podstakannik.delete_file')
def delete_file(request, url, name):
    url, _ = canonicalize_url(url)
    f = get_object_or_404(File, name=name, parent__url=url)
    
    if request.method == 'POST':
        parent = f.parent
        f.delete()
        return HttpResponseRedirect(parent.files_url)

    return render_to_response('podstakannik/delete.html', {'page' : f.parent, 'file' : f}, context_instance=RequestContext(request))
