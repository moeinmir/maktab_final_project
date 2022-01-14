from os import execl
from django.db.models import fields
import django_filters

from .models import *


class ShopTypeFilter(django_filters.FilterSet):

    class Meta:
        model = Shop
        fields = ['category']


class ProductTypeFilter(django_filters.FilterSet):

    class Meta:
        model = ListOfComodity
        fields = {
            'price': ['lt', 'gt'],
            'tag__tag_name': ['exact']
        }
