from audioop import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from projects.models import Category
from re import template

# Create your views here.


class CreateCategory(CreateView):
    model = Category
    template_name = 'superuser/create_category.html'
    fields = "__all__"
    success_url = reverse_lazy('category')


class ListCategory(ListView):
    model = Category
    context_object_name = 'Categories'
    template_name = 'superuser/list_category.html'


class EditCategory(UpdateView):
    model = Category
    template_name = 'superuser/create_category.html'
    queryset = Category.objects.all()
    fields = "__all__"
    success_url = reverse_lazy('categories')


class DeleteCategory(DeleteView):
    model = Category
    pk_ur_kwargs = 'category.id'
    template_name = 'superuser/delete_category.html'
    success_url = reverse_lazy('categories')
