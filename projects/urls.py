from django.urls import path
from .views import EditComment, get_projects, get_project, create_project, CreateComment, DeleteComment, upload_project_images
from django.urls import path, re_path
from .views import CreateComment, DeleteComment, EditComment, get_projects, get_project, create_project, upload_project_images ,CreateDonation


urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:project_id>/', get_project, name='project'),

    path('projects/<int:project_id>/comment_create',CreateComment.as_view(), name="create_comment"),
    path('comments/<pk>', EditComment.as_view(), name='comment'),
    path('comments/delete/<pk>', DeleteComment.as_view(), name='delete_comment'),
    path('upload_images/', upload_project_images, name="upload_project_images"),


    path('projects/<int:project_id>/create_donation',CreateDonation.as_view(), name="create_donation"),
]
