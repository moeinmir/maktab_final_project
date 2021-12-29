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
