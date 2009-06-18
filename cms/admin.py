from django.contrib import admin
from reversion.admin import VersionAdmin
from models import Page, Image, Block

class BlockInline(admin.TabularInline):
    """Inline edit for blocks"""
    model = Block

class PageAdmin(VersionAdmin):
    """Page Admin"""
    inlines = [
        BlockInline,
    ]

admin.site.register(Page, PageAdmin)

class ImageAdmin(admin.ModelAdmin):
    """Image Admin"""
    pass
    
admin.site.register(Image, ImageAdmin)

class BlockAdmin(VersionAdmin):
    """block admin"""
    pass

admin.site.register(Block, BlockAdmin)

