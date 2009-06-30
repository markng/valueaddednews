from django import template
import datetime, time, calendar
register = template.Library()

@register.filter
def fptupletodatetime(tuple):
    """docstring for fptupletodatetime"""
    return datetime.datetime.utcfromtimestamp(calendar.timegm(tuple))
