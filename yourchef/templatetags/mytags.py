from django import template

register = template.Library()

@register.filter
def of5(value, arg):
    return value / arg * 100