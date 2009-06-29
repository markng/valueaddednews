from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from os import path as os_path
import os


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template' : 'construction.html'}, "home"),
    (
        r'^new$', 
        login_required(direct_to_template), 
        {'template' : 'index.html'}, 
        "home2",
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
    (
        r'^images/(.*)$', 
        'django.views.static.serve', 
        {'document_root': os_path.join(settings.PROJECT_PATH, 'media/images')}, 
        'images',
    ),
    (
        r'^js/(.*)$', 
        'django.views.static.serve', 
        {'document_root': os_path.join(settings.PROJECT_PATH, 'media/js')}, 
        'js',
    ),
    (
        r'^uploads/(.*)$', 
        'django.views.static.serve', 
        {'document_root': os_path.join(settings.PROJECT_PATH, 'media/uploads')}, 
        'uploads',
    ),
    (r'^howto/example/1$', 'django.views.generic.simple.direct_to_template', {'template' : 'how_to_1.html'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name' : 'admin/login.html'}),
    (r'^', include('cms.urls')),
)
