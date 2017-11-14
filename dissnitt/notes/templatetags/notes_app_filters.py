from django import template

register = template.Library()

@register.filter(name='sort_by_name')
def sort_by_name(objects):
    return objects.order_by('name')

@register.filter(name='sort_tags_by_count_name')
def sort_tags_by_count_name(objects):
    all_objects, tags = [], []
    count = 0

    objects.sort(key=lambda x: len(x.note_set.all()), reverse=True)

    for i, y in enumerate(objects):
        xcount = len(y.note_set.all())
        if i == 0:
            tags.append(y)
            count = xcount

        elif i == len(objects)-1:
            tags.append(y)
            tags.sort(key=lambda x: x.name)
            all_objects = all_objects + tags

        else:
            if xcount == count:
                tags.append(y)

            else:
                tags.sort(key=lambda x: x.name)
                all_objects = all_objects + tags
                tags = []
                tags.append(y)
                count = xcount

    return all_objects