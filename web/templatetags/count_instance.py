from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def count(value, app_obj):
    instance_count = 0
    for group_obj in app_obj.group.all():
        instance_count += group_obj.instance.count()

    return instance_count