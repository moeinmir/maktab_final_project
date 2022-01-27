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

    path('shop_admin/sell_report/<int:id>',
         SellReport.as_view(), name='sell_report'),

    path('', views.chart, name='sell_chart'),

    path('sell_chart/', views.sell_chart, name='sell_chart_view'),

    # rest

    path('api/user/', UserRegister.as_view(), name='user_register'),
    path('api/user/profile/', ProfileRegister.as_view(), name='profile_register'),
    path('api/shop/', ShopList.as_view(), name='shop_list'),
    path('api/shop/type/', TypeList.as_view(), name='type_list'),
    path('api/shop/<shop_id>/product/',
         ProductList.as_view(), name='product_list'),
    path('api/shop/product/<product_id>/costumer/cart/',
         AddShopBasket.as_view(), name='add_shop_basket'),
    path('api/costumer/order/product/<product_id>/<number>',
         AddOrder.as_view(), name='add_order'),
    path('api/order/<int:id>',
         DeleteOrder.as_view(), name='delete_order'),
    path('api/cart/pay/<int:id>',
         PayShopBasket.as_view(), name='pay_shop_basket'),
    path('api/user/cart/',
         ShopBasketCostumerList.as_view(), name='shop_basket_costumer_list'),

    path('api/user/phoneregister/',
         UserRegisterWithPhone.as_view(), name='user_register_with_phone'),
    path('api/user/otp/<phonenumber>',
         OtpRequest.as_view(), name='otp_request'),

]
