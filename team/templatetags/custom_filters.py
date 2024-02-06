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

@register.filter
def ordinal(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if 10 <= value % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')

    return f"{value}{suffix}"