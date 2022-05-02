from django.urls import path, re_path
from .views import get_projects, get_project


urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/<int:project_id>/', get_project, name='project'),
]
