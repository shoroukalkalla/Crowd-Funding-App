<<<<<<< HEAD
from django.urls import path
from .views import EditComment, get_projects, get_project, create_project ,CreateComment , DeleteComment
=======
from django.urls import path, re_path
from .views import get_projects, get_project, create_project, upload_project_images
>>>>>>> 540a0612a491afa6c42f1f20da6f89d33e88afa0


urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:project_id>/', get_project, name='project'),
<<<<<<< HEAD
    
    path('comment/', CreateComment.as_view(), name='comment'),
    path('comments/<pk>', EditComment.as_view(), name='comment'),
    path('comments/delete/<pk>', DeleteComment.as_view(), name='delete_comment'),
=======
    path('upload_images/', upload_project_images, name="upload_project_images"),

>>>>>>> 540a0612a491afa6c42f1f20da6f89d33e88afa0
]
