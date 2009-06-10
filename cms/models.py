from django.db import models

class Page(models.Model):
    """page object"""
    slug = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)