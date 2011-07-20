from django.db import models
from django import forms
from django.contrib.auth.models import User

from hashlib import md5

# model mixin for figuring out what fields have changed
class DirtyFieldsMixin(models.Model):
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        self._original_state = self._as_dict()

    def _as_dict(self):
        return dict([(f.name, getattr(self, f.name)) for f in self._meta.local_fields if not f.rel])

    def get_dirty_fields(self):
        new_state = self._as_dict()
        return dict([(key, value) for key, value in self._original_state.iteritems() if value != new_state[key]])
    
    def save(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).save(*args, **kwargs)
        self._original_state = self._as_dict()

class File(DirtyFieldsMixin):
    owner = models.ForeignKey(User, related_name='+', null=True)
    
    name = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='uploader/%Y/%m/%d')
    md5 = models.CharField(max_length=32, blank=True)
    size = models.IntegerField(blank=True)
    
    userfields = ['owner', 'name', 'file']
    
    class Meta:
        ordering = ['-date', 'name']
    
    @property
    def nice_size(self):
        # might as well be future-proof
        # binary prefixes, also!
        oom = ['bytes', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        size = self.size
        for i, mag in enumerate(oom):
            if int(size / 1024) == 0:
                return "%i %s" % (round(size), mag)
            size /= 1024
        return "(unknown; > 1024 YiB)"
    
    def get_absolute_url(self):
        return self.file.url
    
    def calculate_file_data(self):
        f = self.file
        f.open('rb')
        m = md5()
        while True:
            d = f.read(8096)
            if not d:
                break
            m.update(d)
        self.md5 = m.hexdigest()
        
        self.size = self.file.size
        if not self.name:
            self.name = self.file.name
    
    def save(self, *args, **kwargs):
        dirty_fields = self.get_dirty_fields()
        if 'file' in dirty_fields:
            self.calculate_file_data()
        super(File, self).save(*args, **kwargs)

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = filter(lambda s: s != 'owner' and s != 'name', File.userfields)
