from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def login_error(request):
    """Error view"""
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    raise ValueError(error_msg)

def redirect(target):
    def redirect_view(request):
        return HttpResponseRedirect(target)
    return redirect_view

def serve_template(tpl):
    def serve_template_view(request):
        return render_to_response(tpl, {}, context_instance=RequestContext(request))
    return serve_template_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gammalevel.views.home', name='home'),
    # url(r'^gammalevel/', include('gammalevel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # root page
    url(r'^$', serve_template('index.html')),
    
    # login and logout
    url(r'^login$', 'social_auth.views.auth', name='socialauth_begin', kwargs={'backend' : 'github'}),
    (r'^logout$', 'django.contrib.auth.views.logout'),
    (r'^login-error$', login_error),
    url(r'^auth/', include('social_auth.urls')),

    # map uploader
    url(r'^upload$', redirect('/uploader/')),
    url(r'^upload/$', redirect('/uploader/')),
    url(r'^uploader$', redirect('/uploader/')),
    url(r'^uploader/', include('uploader.urls')),
    
    # hooks!
    url(r'^hooks/update$', 'oo_extra.views.update'),
    url(r'^hooks/package$', 'oo_extra.views.package_hook'),
)
