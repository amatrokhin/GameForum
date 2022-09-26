from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):                     # replace value of a param in current url
    d = context['request'].GET.copy()                   # need for switching pages without resetting filters
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()