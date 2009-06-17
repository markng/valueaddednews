from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from cms.views import showpage

urlpatterns = patterns('',
    (r'^(?P<path>.*)$', login_required(showpage), {}, "showcmspage"),
)