from django.urls import path, include
from .views import EditComment, get_projects, get_project, create_project, CreateComment, DeleteComment, get_user_donations, upload_project_images, get_user_projects, edit_project
from django.urls import path
from .views import CreateComment, DeleteComment, EditComment,ReportProject, get_projects, get_project, create_project, upload_project_images, CreateDonation,ReportComment,CreateCommentReply,submit_review,delete_rate

from rest_framework import routers


from .views import ProjectViewSet, ProjectImagesViewSet

router = routers.DefaultRouter()
router.register(r'api/projects', ProjectViewSet)
router.register(r'api/images', ProjectImagesViewSet, basename='images')




urlpatterns = [
    path('projects/', get_projects, name='projects'),
    path('projects/user-projects', get_user_projects, name='user_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/<int:project_id>/', get_project, name='project'),
    path('projects/<int:project_id>/edit', edit_project, name='project_edit'),
    path('projects/<int:project_id>/comment_create',
        CreateComment.as_view(), name="create_comment"),
    path('comments/<pk>', EditComment.as_view(), name='comment'),
    path('comments/delete/<pk>', DeleteComment.as_view(), name='delete_comment'),
    path('projects/<int:project_id>/report', ReportProject, name='report_project'),
    path('comments/<int:comment_id>/report', ReportComment, name='report_comment'),
    path('project/<int:user_id>/<int:project_id>/rate', submit_review, name="submit_review"),
    path('project/delete-rate/<int:rate_id>',delete_rate,name="delete_rate"),



    path('upload_images/', upload_project_images, name="upload_project_images"),
    path('', include(router.urls)),


    path('projects/<int:project_id>/create_donation',
        CreateDonation.as_view(), name="create_donation"),
    path('projects/donations',
        get_user_donations, name="donations"),

    path('comments/<pk>/comment_reply_create',
        CreateCommentReply.as_view(), name="create_comment_reply"), 
]