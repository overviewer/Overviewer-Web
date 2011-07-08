from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from mptt.models import MPTTModel, TreeForeignKey
import reversion

# useful decorator to turn a 'string/with///bad/form//' into a canonical url
# ('/string/with/bad/form')
def canonical_url(fn):
    def canonicalize_url(*args, **kwargs):
        url = fn(*args, **kwargs)
        url = filter(lambda s: s != '', url.split('/'))
        return '/' + '/'.join(url)
    return canonicalize_url

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

# a field for storing copyright types
class License(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    image = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

# the biggie -- the page class
class Page(MPTTModel, DirtyFieldsMixin):
    shortname = models.CharField(max_length=40)
    forceurl = models.CharField(max_length=512, blank=True)
    # calculated!
    url = models.CharField(max_length=512, blank=True, editable=False, unique=True, db_index=True)
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    license = models.ForeignKey(License)
    
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    body = models.TextField(blank=True)

    locationfields = ['shortname', 'forceurl', 'parent']
    contentfields = ['title', 'subtitle', 'license', 'body']
    userfields = locationfields + contentfields
    
    def __unicode__(self):
        return self.url
    
    @canonical_url
    def get_calculated_url(self, parent_url=None):
        if self.forceurl:
            return self.forceurl
        
        if self.parent:
            if parent_url is None:
                parent_url = self.parent.calculated_url
            return parent_url + '/' + self.shortname
        
        return self.shortname
    calculated_url = property(get_calculated_url)
    
    def get_absolute_url(self):
        return reverse('podstakannik.views.page', args=(self.url[1:],))
    
    # recalculate current url, and update recursively
    def recalculate_urls(self, parent_url=None):
        new_url = self.get_calculated_url(parent_url=parent_url)
        if new_url == self.url:
            return
        
        self.url = new_url
        
        # do recursive stuff
        for child in self.get_children():
            child.recalculate_urls(parent_url=self.url)
            child.save()
    
    def save(self, *args, **kwargs):
        # recalculate url if shortname or forceurl changes
        dirty_fields = self.get_dirty_fields()
        if 'shortname' in dirty_fields or 'forceurl' in dirty_fields:
            self.recalculate_urls()
        
        super(Page, self).save(*args, **kwargs)
    
reversion.register(Page, fields=Page.userfields)

class PageAddForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = Page.userfields
    
    def save_with_message(self, message, **kwargs):
        user = kwargs.get('user', None)
        if 'user' in kwargs:
            del kwargs['user']
        commit = kwargs.get('commit', True)
        kwargs['commit'] = False
        m = super(PageAddForm, self).save(**kwargs)
        
        #m.full_clean()
        
        if commit:
            with reversion.revision:
                if callable(message):
                    message = message(m)
                reversion.revision.user = user
                reversion.revision.comment = message
                m.save()
        return m
    
    def save(self, **kwargs):
        return self.save_with_message("Initial version.", **kwargs)

class PageEditForm(PageAddForm):
    class Meta(PageAddForm.Meta):
        fields = Page.contentfields + ['message']
        
    message = forms.CharField(max_length=200, required=False)

    def save(self, **kwargs):
        message = self.cleaned_data['message']
        return self.save_with_message(message, **kwargs)

class PageMoveForm(PageAddForm):
    class Meta:
        model = Page
        fields = filter(lambda s: s != 'parent', Page.locationfields)
    
    def save(self, **kwargs):
        return super(PageMoveForm, self).save(**kwargs)
