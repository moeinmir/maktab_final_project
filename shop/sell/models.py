from django.db import models
from django.db.models.fields import PositiveIntegerField


from auser.models import MUser
from post.models import *

shop_status_choices = (('processing', 'processing'),
                       ('confirmed', 'confirmed'), ('deleted', 'deleted'))
comodity_status_choices = (('existing', 'existing'),
                           ('notexisting', 'notexisting'))
basket_status_choices = (('processing', 'processing'),
                         ('confirmed', 'confirmed'), ('payed', 'payed'))


class Shop(models.Model):
    owner = models.ForeignKey(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    status = models.CharField(
        max_length=10, choices=shop_status_choices, default='processing')

    comment_content = models.CharField(max_length=255)
    related_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ListOfComodity(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    price = models.PositiveIntegerField(max_length=10)
    stock = models.PositiveIntegerField(max_length=10)
    status = models.CharField(
        max_length=55, choices=comodity_status_choices, default='existing')
    image = models.ImageField(
        upload_to='uploads', null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    description = models.CharField(max_length=255)


class ShopBasket(models.Model):
    costumer = models.ForeignKey(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    basket_number = PositiveIntegerField(max_length=1)
    total_price = PositiveIntegerField(max_length=10)
    status = models.CharField(
        max_length=55, choices=basket_status_choices, default='processing')
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)


class Order(models.Model):
    costumer = models.ForeignKey(
        MUser, on_delete=models.CASCADE, null=True, blank=True)
    comodity = models.ForeignKey(
        ListOfComodity, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField(max_length=4)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    shop_basket = models.ForeignKey(
        ShopBasket, on_delete=models.CASCADE, null=True, blank=True)
