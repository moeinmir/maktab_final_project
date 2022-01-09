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

    path('api/add_shop_basket/<product_id>',
         AddShopBasket.as_view(), name='add_shop_basket'),
    path('api/add_order/<product_id>/<number>',
         AddOrder.as_view(), name='add_order'),
    path('api/delete_order/<int:id>/',
         DeleteOrder.as_view(), name='delete_order'),
    path('api/pay_shop_basket/<int:id>/',
         PayShopBasket.as_view(), name='pay_shop_basket'),
    path('api/shop_basket_costumer_list/',
         ShopBasketCostumerList.as_view(), name='shop_basket_costumer_list'),
    path('api/open_shop_basket_costumer_list/',
         OpenShopBasketCostumerList.as_view(), name='open_shop_basket_costumer_list'),




    # url(r'^api/add_shop_basket/(?P<product>\d+)/(?P<slug>[\w-]+)/$', AddShopBasket.as_view(), name='add_shop_basket'),
]
