from django.urls import path, re_path
from .views import CreateCategory, ListCategory, EditCategory, DeleteCategory, ListProject, verify_project


urlpatterns = [
    path('category/', CreateCategory.as_view(), name='create_category'),
    path('categories/', ListCategory.as_view(), name='list_category'),
    path('categories/<pk>', EditCategory.as_view(), name='edit_category'),
    path('categories/delete/<pk>', DeleteCategory.as_view(), name='delete_category'),
    path('project/', ListProject.as_view(), name='list_project'),
    path('verifyProject/<int:project_id>',
         verify_project, name='verify_project')
]
