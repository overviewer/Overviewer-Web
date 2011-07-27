from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from podstakannik.models import Page
from uploader.models import File
from reversion.models import Version

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

@receiver(post_save, sender=Page)
def page_message(sender, instance=None, **kwargs):
    if not instance:
        return
    latest = Version.objects.get_for_object(instance).reverse()[0]
    user = latest.revision.user

    url = 'http://overviewer.org' + instance.get_absolute_url()
    if user:
        text = "%s edited '%s' on overviewer.org" % (user.username, instance.title)
    else:
        text = "the page '%s' has been edited on overviewer.org" % (instance.title,)
    Message.send(text, url)
