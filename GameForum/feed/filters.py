from django_filters import FilterSet, DateFilter, ChoiceFilter, CharFilter
from django.forms.widgets import NumberInput
from django.utils.translation import gettext

from .models import Post, Reply, CATEGORIES


class PostsSelfFilter(FilterSet):                # responsible for filters functionalty

    time_in__gt = DateFilter(                    # filer to show posts after certain date
        field_name='time_in',
        lookup_expr='gt',
        label=gettext('Показать посты начиная от'),
        widget=NumberInput(attrs={'type': 'date'}),
    )

    category = ChoiceFilter(                     # filter to show only certain category
        choices=CATEGORIES,
        empty_label='любой'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],              # filter by words/set of symbols in title
        }


class ReplySelfFilter(FilterSet):                # responsible for filters functionalty

    time_in__gt = DateFilter(                    # filer to show replies after certain date
        field_name='time_in',
        lookup_expr='gt',
        label=gettext('Показать посты начиная от'),
        widget=NumberInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Reply
        fields = {
            'text': ['icontains'],              # filter by words/set of symbols in text
            'post__title': ['icontains'],       # filer by reply related post
        }


class ReplyOtherFilter(FilterSet):              # responsible for filters functionalty

    time_in__gt = DateFilter(                   # filer to show replies after certain date
        field_name='time_in',
        lookup_expr='gt',
        label=gettext('Показать посты начиная от'),
        widget=NumberInput(attrs={'type': 'date'}),
    )

    author = CharFilter(                        # sort by author of the reply; insert substring to find matches
        field_name='author__username',
        lookup_expr='icontains'
    )

    class Meta:
        model = Reply
        fields = {
            'text': ['icontains'],              # filter by words/set of symbols in text
            'post__title': ['icontains'],       # filer by reply related post
        }
