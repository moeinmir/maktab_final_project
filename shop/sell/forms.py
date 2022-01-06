from django import forms
from django.db.models import fields
from .models import *
from post.models import *
search_status_choices = (('processing', 'processing'),
                         ('confirmed', 'confirmed'), ('payed', 'payed'), ('all', 'all'))


class NewShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'category', 'delete_status']


class NewProduct(forms.ModelForm):
    class Meta:
        model = ListOfComodity
        fields = ['name', 'tag', 'price', 'primary_stock', 'remaining_stock',
                  'thumbnail', 'description', 'image']


class ShopBasketForm(forms.ModelForm):
    class Meta:
        model = ShopBasket
        fields = ['status']


class ShopBasketSearchForm(forms.ModelForm):

    class Meta:
        model = BasketSearch
        fields = '__all__'


class TagCreateForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


# class ShopBasketSearchForm(forms.Form):
#     status = models.CharField(
#         max_length=55, choices=search_status_choices, default='all')
#     begin_date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(blank=True, null=True)
