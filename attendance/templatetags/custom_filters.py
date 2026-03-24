from django import template

register = template.Library()

@register.filter
def index(List, i):
    return List[i]
from django import template
register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter  
def make_list(value):
    return list(value)

@register.filter
def get_item(mapping, key):
    if isinstance(mapping, dict):
        return mapping.get(key)
    return None
