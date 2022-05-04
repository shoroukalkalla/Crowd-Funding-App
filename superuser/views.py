from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from projects.models import Category, Project
from re import template

# Create your views here.


class CreateCategory(CreateView):
    model = Category
    template_name = 'superuser/create_category.html'
    fields = "__all__"
    success_url = reverse_lazy('list_category')


class ListCategory(ListView):
    model = Category
    context_object_name = 'Categories'
    template_name = 'superuser/list_category.html'


class EditCategory(UpdateView):
    model = Category
    template_name = 'superuser/create_category.html'
    queryset = Category.objects.all()
    fields = "__all__"
    success_url = reverse_lazy('list_category')


class DeleteCategory(DeleteView):
    model = Category
    pk_ur_kwargs = 'category.id'
    template_name = 'superuser/delete_category.html'
    success_url = reverse_lazy('list_category')


class ListProject(ListView):
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.select_related('category', 'user')
    template_name = 'superuser/list_projects.html'


def verify_project(req, project_id):
    Project.objects.filter(id=project_id).update(is_verified=True)
    return redirect(reverse('list_project'))
