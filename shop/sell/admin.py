from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
# admin.site.register(Shop)
# admin.site.register(ListOfComodity)
# admin.site.register(ShopBasket)
# admin.site.register(Order)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('name', 'status')
    search_fields = ('name',)
    fields = (('name', 'owner'), 'category')
    date_hierarchy = ('created_on')


admin.site.register(Shop, ShopAdmin)


class ListOfComodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('name', 'status')
    search_fields = ('name',)
    date_hierarchy = ('created_on')


admin.site.register(ListOfComodity, ListOfComodityAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('costumer', 'comodity')
    list_filter = ('comodity', 'shop_basket')
    search_fields = ('costumer',)
    date_hierarchy = ('created_on')


admin.site.register(Order, OrderAdmin)


class ShopBasketAdmin(admin.ModelAdmin):
    list_display = ('costumer', 'status')
    list_filter = ('costumer', 'status')
    search_fields = ('costumer',)
    date_hierarchy = ('created_on')


admin.site.register(ShopBasket, ShopBasketAdmin)
