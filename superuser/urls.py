from django.urls import path, re_path
from .views import CreateCategory, DeleteProject, DeleteUser, ListCategory, EditCategory, DeleteCategory, ListProject, ListTag, ListUser, verify_project, verify_tag


urlpatterns = [
    path('category/', CreateCategory.as_view(), name='create_category'),
    path('categories/', ListCategory.as_view(), name='list_category'),
    path('categories/<pk>', EditCategory.as_view(), name='edit_category'),
    path('categories/delete/<pk>', DeleteCategory.as_view(), name='delete_category'),
    path('project/', ListProject.as_view(), name='list_project'),
    path('verifyProject/<int:project_id>',
         verify_project, name='verify_project'),
    path('tag/', ListTag.as_view(), name='list_tags'),
    path('verifyTag/<int:id>',
         verify_tag, name='verify_tag'),
    path('project/delete/<pk>', DeleteProject.as_view(), name='delete_project'),
    path('user/', ListUser.as_view(), name='list_users'),
    path('user/delete/<pk>', DeleteUser.as_view(), name='delete_user'),
]
