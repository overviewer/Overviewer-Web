from django.conf.urls.defaults import patterns, include, url

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
    
    # login and logout
    (r'^login$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'', include('social_auth.urls')),

    # fallback on podstakannik page
    url(r'^', include('podstakannik.urls')),
)
