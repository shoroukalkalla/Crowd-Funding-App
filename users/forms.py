from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User
from django import forms


class CustomRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username"
        )


# class CustomLogin(UserChangeForm):

#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ("email", )

class CustomLogin(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
