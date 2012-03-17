from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<username>\w+)$', 'avatarapp.views.getav'),
    (r'^(?P<username>\w+)/body$', 'avatarapp.views.getav'),
    (r'^(?P<username>\w+)/head$', 'avatarapp.views.gethead'),
    (r'^(?P<username>\w+)/bighead$', 'avatarapp.views.getbighead'),
)
