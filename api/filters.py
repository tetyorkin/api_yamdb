import django_filters

from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('year',)
