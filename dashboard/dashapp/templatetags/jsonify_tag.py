from django import template
from json import dumps

register = template.Library()

@register.filter(is_safe=True)
def myjsonify(obj):
    return dumps(obj)
