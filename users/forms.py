from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username"
        )


class CustomLogin(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username")
