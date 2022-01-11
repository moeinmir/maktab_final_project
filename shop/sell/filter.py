
from os import execl
import django_filters

from .models import *


class ShopTypeFilter(django_filters.FilterSet):
    # creator_isnull = django_filters.BoleanFilter(field_name='creator', lookup_expr='isnull')
    class Meta:
        model = Shop
        fields = ['category']


class ProductTypeFilter(django_filters.FilterSet):
    # creator_isnull = django_filters.BoleanFilter(field_name='creator', lookup_expr='isnull')
    class Meta:
        model = ListOfComodity
        exclude = ['image', 'thumbnail']
