from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<username>\w+)$', 'avatarapp.views.getav'),
)
