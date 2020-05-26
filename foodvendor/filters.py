import django_filters
from .models import Menu, MenuItem, Order


class MenuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Menu
        fields = ('name',)
        labels = {
            'name': 'Food',
        }