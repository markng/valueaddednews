from django.db import models

class Page(models.Model):
    """page object"""
    slug = models.CharField(max_length=255, unique=True, null=True)
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
    
    def get_ancestors(self, ancestors=None, reverse=True):
        """get a list of ancestor pages"""
        if not ancestors:
            ancestors=[]
        if self.parent:
            if reverse:
                ancestors.insert(0, self.parent)
            else:
                ancestors.append(self.parent)
            ancestors = self.parent.get_ancestors(ancestors=ancestors, reverse=reverse)
        return ancestors

class Image(models.Model):
    """image object"""
    name = models.CharField(max_length=255, unique=True)
    caption = models.TextField()
    image = models.ImageField(upload_to='images')