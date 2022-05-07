from django.urls import path
from .views import Edit_comment, get_projects, get_project, create_project ,CreateComment , DeleteComment


urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:project_id>/', get_project, name='project'),
    
    path('comment/', CreateComment.as_view(), name='comment'),
    path('comments/<int:comment_id>', Edit_comment, name='comment'),
    # path('comments/<pk>', EditComment.as_view(), name='comment'),
    path('comments/delete/<pk>', DeleteComment.as_view(), name='delete_comment'),
]
