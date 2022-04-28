from django.db import models
from django.forms import ImageField

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=350)
    mobile_phone = models.CharField(max_length=150)
    avatar = models.ImageField(
        upload_to="users", height_field=None, width_field=None, max_length=100)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    facebook_profile = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
