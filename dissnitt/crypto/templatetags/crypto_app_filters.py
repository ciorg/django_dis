from django import template

register = template.Library()

@register.filter(name='make_usd')
def make_usd(objects):
    return "{:,.2f}".format(objects)