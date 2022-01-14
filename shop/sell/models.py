from logging import exception
from os import name, truncate
from django.db import models
from django.db.models.fields import PositiveIntegerField
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
from auser.models import MUser
from post.models import *
from datetime import date

shop_status_choices = (('processing', 'processing'),
                       ('confirmed', 'confirmed'))
delete_status_choice = (('delete', 'delete'), ('undelete', 'undelete'))


comodity_status_choices = (('existing', 'existing'),
                           ('notexisting', 'notexisting'))
basket_status_choices = (('processing', 'processing'),
                         ('confirmed', 'confirmed'), ('payed', 'payed'), ('canceled', 'canceled'))

search_status_choices = (('processing', 'processing'),
                         ('confirmed', 'confirmed'), ('payed', 'payed'), ('all', 'all'))


class Shop(models.Model):
    owner = models.OneToOneField(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    status = models.CharField(
        max_length=10, choices=shop_status_choices, default='processing')
    delete_status = models.CharField(
        max_length=10, choices=delete_status_choice, default='undelete')

    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ListOfComodity(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    price = models.PositiveIntegerField()
    primary_stock = models.PositiveIntegerField()
    status = models.CharField(
        max_length=55, choices=comodity_status_choices, default='existing')
    thumbnail = models.ImageField(
        upload_to='uploads', null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='uploads', null=True, blank=True)
    remaining_stock = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.remaining_stock > 0:
            self.status = 'existing'
            super().save(*args, **kwargs)
        else:
            self.status = 'notexisting'
            super().save(*args, **kwargs)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            _thumbnail = get_thumbnail(self.thumbnail,
                                       '300x300',
                                       upscale=False,
                                       crop=False,
                                       quality=100)
            return format_html('<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
        return ""


class ShopBasket(models.Model):
    costumer = models.ForeignKey(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    total_price = PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=55, choices=basket_status_choices, default='processing')
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True)


class Order(models.Model):
    costumer = models.ForeignKey(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    comodity = models.ForeignKey(
        ListOfComodity, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    shop_basket = models.ForeignKey(
        ShopBasket, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        price = self.comodity.price
        if self.comodity.remaining_stock >= int(self.number):
            self.shop_basket.total_price += int(self.number)*price
            self.shop_basket.save()
            self.comodity.remaining_stock -= int(self.number)
            self.comodity.save()
            self.costumer = self.shop_basket.costumer
            super(Order, self).save(*args, **kwargs)


class BasketSearch(models.Model):
    status = models.CharField(
        max_length=55, choices=search_status_choices, default='all')
    begin_date = models.DateField(default=date(1500, 10, 10), blank=True)
    end_date = models.DateField(default=date(2500, 10, 10), blank=True)


class Profile(models.Model):
    image = models.ImageField(
        upload_to='uploads', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    interest = models.CharField(max_length=255, null=True, blank=True)
    costumer = models.OneToOneField(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
