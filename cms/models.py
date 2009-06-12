from django.db import models

class Page(models.Model):
    """page object"""
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        """unicode repr"""
        return "%s : ( %s )" % (self.title, self.slug)
    
    def get_absolute_url(self):
        """docstring for get_absolute_url"""
        return '/%s' % (self.slug)