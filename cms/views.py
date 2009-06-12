from models import Page
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

def showpage(request, path='', template_name=None):
    """docstring for showpage"""
    try:
        page = Page.objects.filter(published=True).get(slug=path)
    except Page.DoesNotExist, e:
        raise Http404
    if not template_name:
        template_name = 'cms/standard.html' # todo - add template field to model and choose from that
    
    responsed = {}
    responsed['page'] = page
    
    if page.parent:
        # is a child of something
        responsed['parent'] = page.parent
        responsed['siblings'] = page.parent.children.all()
    responsed['children'] = page.children.all()
    
    return render_to_response(template_name, responsed)
    