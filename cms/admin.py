from django.contrib import admin
from models import Page

class PageAdmin(admin.ModelAdmin):
    """Page Admin"""
    pass

admin.site.register(Page, PageAdmin)