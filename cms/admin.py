from django.contrib import admin
from reversion.admin import VersionAdmin
from models import Page

class PageAdmin(VersionAdmin):
    """Page Admin"""
    pass

admin.site.register(Page, PageAdmin)