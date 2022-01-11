from django.contrib.auth import get_user_model
from rest_framework import serializers

from auser.models import *
from .models import *
from post.models import *

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUser
        fields = ['id', 'username', 'email', 'password', 'phonenumber']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'first_name',
                  'last_name', 'profession', 'interest']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'category']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfComodity
        fields = '__all__'


class ShopBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBasket
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
