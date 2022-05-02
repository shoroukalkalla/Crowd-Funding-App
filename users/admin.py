from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomLogin, CustomRegistration
from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomRegistration
    # form = CustomLogin
    model = User
    list_display = ["email", "username", ]


admin.site.register(User, CustomUserAdmin)
