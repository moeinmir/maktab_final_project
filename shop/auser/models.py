from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, PositiveIntegerField

USER_CHOICE = (('Shop', 'Shop'), ('costumer', 'costumer'))


class MUser(AbstractUser):
    user_type = CharField(
        max_length=10, choices=USER_CHOICE, default='costumer')
    phonenumber = PositiveIntegerField(null=True, blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phonenumber = models.CharField(
        validators=[phone_regex], max_length=17, null=True, blank=True)


my_user_model = MUser


class MyPhoneBackend(object):
    """
    Custom Email Backend to perform authentication via email
    """
    # print('fffffffffffffffffffffffffff')

    def authenticate(self, request, username=None, password=None, **kwargs):
        print('fffffffffffffffffffffffffff')
        my_user_model = get_user_model()
        try:
            print('ggggggggggggggggg')
            print('fff')
            user = my_user_model.objects.get(phonenumber=username)
            print(user)
            print('ddd')
            if user.check_password(password):
                return user  # return user on valid credentials
        except my_user_model.DoesNotExist:
            return None  # return None if custom user model does not exist
        except:
            return None  # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None



