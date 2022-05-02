from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)

    # first_name = models.CharField(max_length=250)
    # last_name = models.CharField(max_length=250)
    # password = models.CharField(max_length=350)
    mobile_phone = models.CharField(max_length=150)
    avatar = models.ImageField(
        upload_to="users", height_field=None, width_field=None, max_length=100)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    facebook_profile = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
