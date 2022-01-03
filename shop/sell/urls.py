from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'sell'

urlpatterns = [
    path('shop_admin/<int:id>',
         ShopAdmin.as_view(template_name='shop_admin.html'), name='shop_admin'),
    path('shop_admin/shop_register/<int:id>',
         ShopRegister.as_view()),
    path('shop_admin/add_product/<int:id>',
         AddProduct.as_view()),
    path('shop_admin/shop_basket/<int:id>',
         ShopBasketView.as_view()),

]
