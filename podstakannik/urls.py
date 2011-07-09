from django.conf.urls.defaults import patterns
from views import list_files, delete_file, file, add, edit, move, delete, history, page

urlpatterns = patterns('',
                       (r'^(?P<url>.*).files$', list_files),
                       (r'^(?P<url>.*)/files/(?P<name>.*)/delete$', delete_file),
                       (r'^(?P<url>.*)/files/(?P<name>.*)$', file),
                       
                       (r'^(?P<url>.*)/add$', add),
                       (r'^(?P<url>.*)/edit$', edit),
                       (r'^(?P<url>.*)/move$', move),
                       (r'^(?P<url>.*)/delete$', delete),
                       (r'^(?P<url>.*).history$', history),
                       
                       (r'^(?P<url>.*)$', page),
)
