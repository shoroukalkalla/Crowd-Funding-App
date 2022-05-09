from django.contrib import admin
from .models import Category, Project, Tag, Donation


admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Donation)

