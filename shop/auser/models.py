import email
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
    phonenumber = PositiveIntegerField(null=True, blank=True, unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phonenumber = models.CharField(
        validators=[phone_regex], max_length=17, null=True, blank=True)


my_user_model = MUser


class MyPhoneBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(phonenumber=username)
            print(user)
            if user.check_password(password):
                return user
        except my_user_model.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None


class MyEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(email=username)
            print(user)
            if user.check_password(password) and user.user_type == 'costumer':
                return user
        except my_user_model.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
