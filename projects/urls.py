from django.urls import path, re_path
from .views import get_projects


urlpatterns = [
    path('projects', get_projects, name='projects')
]
