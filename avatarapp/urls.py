from django.conf.urls import *

urlpatterns = patterns('',
    (r'^(?P<username>(\w|\s)+)$', 'avatarapp.views.getav'),
    (r'^(?P<username>(\w|\s)+)/body$', 'avatarapp.views.getav'),
    (r'^(?P<username>(\w|\s)+)/head$', 'avatarapp.views.gethead'),
    (r'^(?P<username>(\w|\s)+)/bighead$', 'avatarapp.views.getbighead'),
)
