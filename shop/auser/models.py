from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class MUser(AbstractUser):
    is_shop = models.BooleanField(
        'student status', default=False)
    is_costumer = models.BooleanField(
        'teacher status', default=False)
