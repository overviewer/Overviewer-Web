from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from uploader.models import File

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
