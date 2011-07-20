from django.conf.urls.defaults import patterns
from views import upload_progress, upload, list_uploads, delete

urlpatterns = patterns('',
                       (r'^delete/([0-9]+)$', delete),
                       (r'^progress$', upload_progress),
                       (r'^list$', list_uploads),
                       (r'^$', upload),
)
