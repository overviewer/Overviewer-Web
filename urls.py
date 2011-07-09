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

    # fallback on podstakannik page
    (r'^(?P<url>.*).files$', 'podstakannik.views.list_files'),
    (r'^(?P<url>.*)/files/(?P<name>.*)/delete$', 'podstakannik.views.delete_file'),
    (r'^(?P<url>.*)/files/(?P<name>.*)$', 'podstakannik.views.file'),

    (r'^(?P<url>.*)/add$', 'podstakannik.views.add'),
    (r'^(?P<url>.*)/edit$', 'podstakannik.views.edit'),
    (r'^(?P<url>.*)/move$', 'podstakannik.views.move'),
    (r'^(?P<url>.*)/delete$', 'podstakannik.views.delete'),
    (r'^(?P<url>.*).history$', 'podstakannik.views.history'),

    (r'^(?P<url>.*)$', 'podstakannik.views.page'),
)
