from django.urls import path, re_path
from .views import get_projects, get_project, create_project, upload_project_images


urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:project_id>/', get_project, name='project'),
    path('upload_images/', upload_project_images, name="upload_project_images"),

]
