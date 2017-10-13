from django import template

register = template.Library()

@register.filter(name='sort_by_name')
def sort_by_name(objects):
    return objects.order_by('name')