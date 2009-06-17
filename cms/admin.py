from django.contrib import admin
from reversion.admin import VersionAdmin
from models import Page, Image

class PageAdmin(VersionAdmin):
    """Page Admin"""
    pass

admin.site.register(Page, PageAdmin)

class ImageAdmin(admin.ModelAdmin):
    """Image Admin"""
    pass
    
admin.site.register(Image, ImageAdmin)