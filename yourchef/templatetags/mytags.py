from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def of5(value, arg):
    return value / arg * 100

@register.filter
@stringfilter
def namespace(value, arg):
    return arg + "/" + value