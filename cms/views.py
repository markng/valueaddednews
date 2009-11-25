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
        if page.template:
            template_name = page.template
        else:
            template_name = 'cms/standard.html'
    responsed = {}
    responsed['page'] = page

    if page.parent:
        # is a child of something
        responsed['parent'] = page.parent
        responsed['toptitle'] = page.parent.title
        responsed['siblings'] = page.parent.children.all()
    else:
        # parent or standalone
        responsed['toptitle'] = page.title
    responsed['children'] = page.children.all()

    blocks = {}
    for block in page.blocks.all():
        blocks[block.name] = block
    responsed['blocks'] = blocks

    return render_to_response(template_name, responsed)

def missingpage(request):
    """404 handler"""
    return render_to_response('404.html')