from django import forms
from django.db.models import fields
from .models import *


class NewShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'category']


class NewProduct(forms.ModelForm):
    class Meta:
        model = ListOfComodity
        fields = ['name', 'tag', 'price', 'stock',
                  'thumbnail', 'description', 'image']


class ShopBasketForm(forms.ModelForm):
    class Meta:
        model = ShopBasket
        fields = ['status']


class ShopBasketSearchForm(forms.ModelForm):

    class Meta:
        model = BasketSearch
        fields = '__all__'
