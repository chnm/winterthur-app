from django import template

# this is all temporary
register = template.Library()


@register.filter
def getallattrs(value):
    return dir(value)
