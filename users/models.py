from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.urls import reverse


# Create your models here.


class User(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)

    mobile_phone = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="users", default="users/default.png")
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    facebook_profile = models.CharField(max_length=150)
    country = CountryField(blank_label='select country')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):

        return reverse('profile', args=[self.id])
