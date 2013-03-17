from django.db import models

import datetime
from django import forms

from django.db.models.signals import post_save
from django.dispatch import receiver
from uploader.models import File

class Package(models.Model):
    platform = models.CharField(max_length=64)
    repo = models.CharField(max_length=200)
    checkout = models.CharField(max_length=64)
    commit = models.CharField(max_length=128)
    date = models.DateTimeField()
    url = models.URLField()
    
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    revision = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['-date', '-major', '-minor', '-revision', 'platform', 'checkout', 'repo']
    
    @property
    def version(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.revision)
    
    def get_absolute_url(self):
        return self.url
    
    def __unicode__(self):
        return '{0} {1}'.format(self.platform, self.version)

class PackageModelForm(forms.ModelForm):
    version = forms.CharField(max_length=64)
    
    class Meta:
        model = Package
        fields = ('platform', 'repo', 'checkout', 'commit', 'version', 'url')
    
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs.keys():
            if not 'initial' in kwargs.keys():
                kwargs['initial'] = {}
            
            kwargs['initial']['version'] = kwargs['instance'].version
        super(PackageModelForm, self).__init__(*args, **kwargs)
    
    def clean_version(self):
        version = self.cleaned_data['version']
        try:
            version = map(int, version.split('.'))
            if not len(version) == 3:
                raise ValueError('version does not have 2 dots')
        except ValueError:
            raise forms.ValidationError('invalid version string (form #.#.#)')
        return self.cleaned_data['version']
    
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(PackageModelForm, self).save(commit=False)
        
        m.major, m.minor, m.revision = map(int, self.cleaned_data['version'].split('.'))
        m.date = datetime.datetime.now()
        m.full_clean()
        
        if commit:
            m.save()
        return m

class Build(models.Model):
    builder = models.CharField(max_length=64)
    buildnumber = models.PositiveIntegerField()
    repo = models.CharField(max_length=200)
    branch = models.CharField(max_length=64)
    commit = models.CharField(max_length=128)
    project = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=200)
    downloads = models.PositiveIntegerField(default=0)
    
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    revision = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['-date', '-major', '-minor', '-revision', 'builder', '-buildnumber', 'project']
    
    @property
    def version(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.revision)
    
    def get_absolute_url(self):
        #return reverse('oo_extra.views.build', kwargs=dict(bid=self.pk, path=self.path))
        # buildbot needs this to not use reverse
        # sorry! maybe I'll work out how to do this right later
        # also the ext calculation is highly-dependent on path format
        try:
            ext = self.path.rsplit('-', 1)[1]
            ext = ext.split('.', 1)[1]
            ext = '.' + ext
        except Exception:
            ext = ''
            
        builder = self.builder
        if builder == 'src':
            builder = ''
        else:
            builder = '-' + builder
            
        nice_path = '{project}-{version}{builder}{ext}'.format(project=self.project, version=self.version, builder=builder, ext=ext)
        
        return 'http://overviewer.org/builds/{0}/{1}'.format(self.pk, nice_path)
    
    def __unicode__(self):
        return '{0} {1} ({2}:{3})'.format(self.project, self.version, self.builder, self.buildnumber)

class BuildModelForm(forms.ModelForm):
    version = forms.CharField(max_length=64)
    
    class Meta:
        model = Build
        fields = ('builder', 'buildnumber', 'repo', 'branch', 'commit', 'project', 'version', 'path')
    
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs.keys():
            if not 'initial' in kwargs.keys():
                kwargs['initial'] = {}
            
            kwargs['initial']['version'] = kwargs['instance'].version
        super(BuildModelForm, self).__init__(*args, **kwargs)
    
    def clean_version(self):
        version = self.cleaned_data['version']
        try:
            version = map(int, version.split('.'))
            if not len(version) == 3:
                raise ValueError('version does not have 2 dots')
        except ValueError:
            raise forms.ValidationError('invalid version string (form #.#.#)')
        return self.cleaned_data['version']
    
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(PackageModelForm, self).save(commit=False)
        
        m.major, m.minor, m.revision = map(int, self.cleaned_data['version'].split('.'))
        m.date = datetime.datetime.now()
        m.full_clean()
        
        if commit:
            m.save()
        return m

class Message(models.Model):
    text = models.CharField(max_length=512)
    url = models.URLField(blank=True, null=True)
    
    def __unicode__(self):
        if self.url:
            return "%s (%s)" % (self.text, self.url)
        return self.text
    
    @classmethod
    def send(cls, text, url=None):
        m = cls(text=text, url=url)
        m.save()
        return m

@receiver(post_save, sender=File)
def file_message(sender, instance=None, **kwargs):
    if not instance:
        return
    
    url = 'http://overviewer.org/uploader/list'
    if instance.owner:
        text = "%s uploaded file '%s' on overviewer.org" % (instance.owner.username, instance.name)
    else:
        text = "a file '%s' has been uploaded on overviewer.org" % (instance.name,)
    Message.send(text, url)
