from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, PositiveIntegerField


class MUser(AbstractUser):
    is_shop = models.BooleanField(
        'student status', default=False)
    is_costumer = models.BooleanField(
        'teacher status', default=False)
    phonenumber = PositiveIntegerField(max_length=11, null=True, blank=True)
