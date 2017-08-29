from django import template

register = template.Library()

@register.filter(name='sort_by_done')
def sort_by_done(objects):
    return objects.order_by('completed', 'priority')
