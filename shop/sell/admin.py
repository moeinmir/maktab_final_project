from django.contrib import admin
# Register your models here.
from .models import *

# Register your models here.
# admin.site.register(Shop)
# admin.site.register(ListOfComodity)
# admin.site.register(ShopBasket)
# admin.site.register(Order)


@admin.action(description='confirm')
def confirm(modeladmin, request, queryset):
    queryset.update(status='confirmed')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_filter = ('name', 'status', 'delete_status')
    search_fields = ('name',)
    fields = (('name', 'owner'), 'category')
    date_hierarchy = ('created_on')
    list_editable = ('status',)
    actions = [confirm]


admin.site.register(Shop, ShopAdmin)


def make_published(Shop, request, queryset):
    queryset.update(status='p')


class ListOfComodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'thumbnail_preview')
    list_filter = ('name', 'status')
    search_fields = ('name',)
    date_hierarchy = ('created_on')

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


admin.site.register(ListOfComodity, ListOfComodityAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('costumer', 'comodity')
    list_filter = ('comodity', 'shop_basket')
    search_fields = ('costumer',)
    date_hierarchy = ('created_on')


admin.site.register(Order, OrderAdmin)


class ShopBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'costumer', 'status')
    list_filter = ('costumer', 'status')
    search_fields = ('costumer',)
    date_hierarchy = ('created_on')


admin.site.register(ShopBasket, ShopBasketAdmin)


admin.site.register(BasketSearch)
