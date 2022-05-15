# from asyncio.windows_events import NULL
from pyexpat import model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from projects.models import Category, CommentReport, Donation, Project, Tag, ProjectReport
from re import template
from django.db.models import Q

from users.models import User

# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import add_message, INFO, ERROR


class CreateCategory(PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'superuser/create_category.html'
    fields = "__all__"
    success_url = reverse_lazy('list_category')
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListCategory(PermissionRequiredMixin, ListView):
    model = Category
    context_object_name = 'Categories'
    template_name = 'superuser/list_category.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class EditCategory(PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'superuser/create_category.html'
    queryset = Category.objects.all()
    fields = "__all__"
    success_url = reverse_lazy('list_category')
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class DeleteCategory(PermissionRequiredMixin, DeleteView):
    model = Category
    pk_ur_kwargs = 'category.id'
    template_name = 'superuser/delete_category.html'
    success_url = reverse_lazy('list_category')
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListProject(PermissionRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.select_related('category', 'user')
    template_name = 'superuser/list_projects.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


def verify_project(req, project_id):
    Project.objects.filter(id=project_id).update(is_verified=True)
    return redirect(reverse('list_project'))


class ListTag(PermissionRequiredMixin, ListView):
    model = Tag
    context_object_name = 'tags'
    queryset = Tag.objects.select_related('project')
    template_name = 'superuser/list_tags.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")
# -------------------Tags---------------------------#


def get_tags(request):
    tags_query = Tag.objects.all()
    tags = []
    for tag in tags_query:
        tag_project = tag.project_set.values_list('id', 'title')
        if tag_project:
            project_tag = {
                'tag': tag,
                'project': tag_project
            }
            tags.append(project_tag)

    context = {
        'project_tags': tags,
    }
    return render(request, 'superuser/list_tags.html', context)

# ----------------------------------------------------#


def verify_tag(req, pk):
    tag = Tag.objects.get(pk=pk)
    tag.is_verified = True
    tag.save()
    return redirect(reverse('list_tags'))


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    pk_ur_kwargs = 'project.id'
    template_name = 'superuser/delete_category.html'
    success_url = reverse_lazy('list_project')
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListUser(PermissionRequiredMixin, ListView):
    model = User
    # context_object_name = 'users'
    template_name = 'superuser/list_users.html'
    permission_required = 'user.is_superuser'

    def get_context_data(self, **kwargs):
        context = super(ListUser, self).get_context_data(**kwargs)
        users = User.objects.filter(is_superuser=0).all()
        context['users'] = users
        return context

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class DeleteUser(PermissionRequiredMixin, DeleteView):
    model = User
    pk_ur_kwargs = 'user.id'
    template_name = 'superuser/delete_category.html'
    success_url = reverse_lazy('list_users')
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListProjectsReport(PermissionRequiredMixin, ListView):
    model = ProjectReport
    context_object_name = 'reports'
    template_name = 'superuser/list_reports.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListProjectsCommentReport(PermissionRequiredMixin, ListView):
    model = CommentReport
    context_object_name = 'commentReports'
    template_name = 'superuser/list_comment_reports.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")


class ListProjectsDonations(PermissionRequiredMixin, ListView):
    model = Donation
    context_object_name = 'donations'
    template_name = 'superuser/list_donations.html'
    permission_required = 'user.is_superuser'

    def handle_no_permission(self):
        add_message(self.request, ERROR,
                    'You are not allowed to open this link')
        return redirect("/")
