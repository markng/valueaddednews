from django.conf.urls.defaults import *
from django.conf import settings
from os import path as os_path
import os


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^valueaddednews/', include('valueaddednews.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (
        r'^$', 
        'django.views.generic.simple.direct_to_template', 
        {'template' : 'index.html'}, 
        "home",
    ),
    (
        r'^images/(.*)$', 
        'django.views.static.serve', 
        {'document_root': os_path.join(settings.PROJECT_PATH, 'media/images')}, 
        'images',
    ),
    (
        r'^css/(.*)$', 
        'django.views.static.serve', 
        {'document_root': os_path.join(settings.PROJECT_PATH, 'media/css')}, 
        'css',
    ),
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('cms.urls')),
)
