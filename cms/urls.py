from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<path>.*)$', 'cms.views.showpage', {}, "showcmspage"),
)