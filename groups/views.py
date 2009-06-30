from django.conf import settings
from django.shortcuts import render_to_response
import feedparser

def list(request):
    """show list of messages in the group"""
    # you'll want to cache this page
    parsed = feedparser.parse(settings.GROUP_ADDRESS + 'feed/atom_v1_0_topics.xml?num=5')
    totemplate = {
        'messages' : parsed.entries,
    }
    return render_to_response('groups/list.html', totemplate)