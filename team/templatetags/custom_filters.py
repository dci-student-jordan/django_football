# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)

@register.filter
def return_id(l, i):
    try:
        return l[i]
    except:
        return None
