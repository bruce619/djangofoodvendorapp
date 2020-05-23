import django_filters
from .models import Menu, MenuItem, Order


class MenuFilter(django_filters.FilterSet):

    class Meta:
        model = Menu
        fields = ('name',)
        labels = {
            'name': 'Food',
        }