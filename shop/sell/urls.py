from django.urls import path
from django.urls import include, path
from django.views.generic import TemplateView
from .views import *
# rest

from . import views


app_name = 'sell'

urlpatterns = [
    path('shop_admin/<int:id>',
         ShopAdmin.as_view(template_name='shop_admin.html'), name='shop_admin'),
    path('shop_admin/shop_register/<int:id>',
         ShopRegister.as_view()),
    path('shop_admin/add_product/<int:id>',
         AddProduct.as_view()),
    path('shop_admin/shop_basket/<int:id>',
         ShopBasketView.as_view(), name='shop_basket'),
    path('shop_admin/shop_basket/shop_basket_details/<int:id>',
         ShopBasketDetailView.as_view(), name='shop_basket_details'),
    path('shop_admin/shop_edit/<int:id>',
         ShopEditView.as_view(), name='shop_edit'),

    path('shop_admin/comodity_list_view/<int:id>',
         ComodityListView.as_view(), name='comodity_list_view'),
    # rest

    path('api/user/', UserRegister.as_view(), name='user_register'),

    path('api/profile/', ProfileRegister.as_view(), name='profile_register'),

    path('api/shop_list/', ShopList.as_view(), name='shop_list'),

    path('api/type_list/', TypeList.as_view(), name='type_list'),

    path('api/product_list/', ProductList.as_view(), name='product_list'),

    path('api/add_shop_basket/', AddShopBasket.as_view(), name='add_shop_basket'),
]
