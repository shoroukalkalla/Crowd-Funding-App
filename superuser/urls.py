from django.urls import path, re_path
from .views import CreateCategory, ListCategory, EditCategory, DeleteCategory


urlpatterns = [
    path('category/', CreateCategory.as_view(), name='category'),
    path('categories/', ListCategory.as_view(), name='categories'),
    path('categories/<pk>', EditCategory.as_view(), name='category'),
    path('categories/delete/<pk>', DeleteCategory.as_view(), name='delete_category'),
]
