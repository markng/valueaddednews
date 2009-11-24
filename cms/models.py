from django.db import models
import reversion

TEMPLATE_CHOICES = (
    ('cms/standard.html', 'Standard Page'),
    ('cms/category.html', 'Category Page'),
    ('cms/standalone-standard.html', 'Standard Page - standalone'),
)

class Page(models.Model):
    """page object"""
    slug = models.CharField(max_length=255, unique=True, null=True)
    title = models.CharField(max_length=255)
    template = models.CharField(max_length=255, choices=TEMPLATE_CHOICES, null=True)
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

class Block(models.Model):
    """content block"""
    name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    page = models.ForeignKey(Page, related_name='blocks', blank=True)

    def __unicode__(self):
        """string repr"""
        return self.name
reversion.register(Page, follow=["blocks"])
reversion.register(Block)


class Image(models.Model):
    """image object"""
    name = models.CharField(max_length=255, unique=True)
    caption = models.TextField()
    image = models.ImageField(upload_to='images')

    def __unicode__(self):
        """string repr"""
        return self.name