from django.db import models

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
