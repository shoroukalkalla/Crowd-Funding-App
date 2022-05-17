from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from pyexpat import model
from django.forms import ValidationError
from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProjectForm
from .models import Comment, CommentReply, ProjectImage, Tag, Project, Donation, ProjectRate
from users.models import User

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.http import Http404
from django.core.exceptions import PermissionDenied


from .serializers import ProjectSerializer, ProjectImagesSerializer

from requests import request
from django.contrib import messages

from .forms import ProjectForm, ProjectReports, CommentReport, ProjectRateForm
from .models import Comment, ProjectImage, Tag, Project, Donation, ProjectReport, ProjectImage, ProjectRate
from users.models import User


# Create your views here.

def get_project_data(project_id, are_projects = False):
    project = get_object_or_404(Project, id=project_id)
    user = User.objects.get(id=project.user.id)
    if(are_projects):
        images = ProjectImage.objects.filter(project_id=project.id).first()
    else:    
        images = ProjectImage.objects.filter(project_id=project.id)
    num_of_Projects = user.project_set.count()
    amount = Donation.objects.filter(
        project_id=project.id).aggregate(Sum('donation_amount'))
    donators = Donation.objects.filter(
        project_id=project.id).values('donator').distinct().count()
    comments = Comment.objects.filter(project_id=project_id).order_by('-id')
    commentReplies = CommentReply.objects.all().order_by('-id')
    reviews = ProjectRate.objects.filter(project_id=project_id)

    data = {'project': project, 'project_user': user, 'images': images, "num_of_Projects": num_of_Projects,
            'donation_amount': amount['donation_amount__sum'], 'donators': donators, 'comments': comments, 'commentReplies': commentReplies, 'reviews': reviews}
    return data



def get_projects(request):
    project_array = []

    projects = Project.objects.all().values('id')
  
    for project in projects:
        data = get_project_data(project['id'],True)
        project_array.append(data)
    project_paginator=Paginator(project_array,6)
    page_num=request.GET.get('page')
    page=project_paginator.get_page(page_num)

    return render(request, 'projects/projects.html', {'page': page})


def get_project(request, project_id):
    context = get_project_data(project_id)
    return render(request, 'projects/project.html', context)


@login_required
def get_user_projects(request):
    project_array = []

    projects = Project.objects.filter(user_id=request.user.id).values('id')
    for project in projects:
        data = get_project_data(project['id'],True)
        project_array.append(data)
    project_paginator=Paginator(project_array,6)
    page_num=request.GET.get('page')
    page=project_paginator.get_page(page_num)

    return render(request, 'projects/user_projects.html', {'page': page})


@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        # fetching Images
        # images = request.FILES.getlist('images')
        images = request.POST['images'].split()
        # Adding New Tags
        retags = request.POST.getlist('tags[]')
        for tag in retags:
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create(name=tag, is_verified=False)
        # Creating new Project
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            # saving tages
            for tag in retags:
                project.tags.add(Tag.objects.get(name=tag))
            project.save()
            # saving images
            for img in images:
                ProjectImage.objects.create(
                    image=f"projects/images/{img}", project=project)

        return redirect('project', project_id=project.id)

    project_form = ProjectForm()
    verifiedTags = Tag.objects.filter(is_verified=True)
    context = {'project_form': project_form, 'tags': verifiedTags}

    return render(request, "projects/project_create.html", context)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    verified_tags = Tag.objects.filter(is_verified=True)
    project_tags = project.tags.all()
    project_form = ProjectForm(instance=project)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        # fetching Images
        # images = request.FILES.getlist('images')
        images = request.POST['images'].split()
        deleted_images = request.POST['ids'].split(',')
        
        if(deleted_images != ['']):
            for img in deleted_images:
                ProjectImage.objects.get(id=img).delete()
        # Adding New Tags
        retags = request.POST.getlist('tags[]')
        for tag in retags:
            print(tag)
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create(name=tag, is_verified=False)
        # Creating new Project
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            # saving tages
            project.tags.clear()
            for tag in retags:
                project.tags.add(Tag.objects.get(name=tag))
            project.save()
            # saving images
            for img in images:
                ProjectImage.objects.create(
                    image=f"projects/images/{img}", project=project)

        return redirect('project', project_id=project.id)
    else:

        context = {'project_form': project_form, 'tags': verified_tags,
                   'project': project, 'project_tags': project_tags}

        if request.user.id == project.user.id :
            return render(request, "projects/project_edit.html", context)
        else:
            raise PermissionDenied()


# -------------------------------------------------------------#

class CreateComment(SuccessMessageMixin, CreateView):
    model = Comment
    # template_name = 'projects/project.html'

    fields = ["comment", "project"]

    def get_success_url(self):
        url = self.request.get_full_path()
        url = url.split("/")
        url.pop()
        url = "/".join(url)

        return f"{url}#comments"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CreateComment, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Comment was created"


class EditComment(SuccessMessageMixin, UpdateView):
    model = Comment
    # template_name = 'projects/project.html'
    fields = ["comment", "project"]
    pk_ur_kwargs = 'comment.id'

    def get_success_url(self):
        return f"/projects/{self.request.POST['project']}#comment{self.kwargs['pk']}"
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(EditComment, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Comment was updated"


class DeleteComment(SuccessMessageMixin, DeleteView):
    model = Comment

    def get_success_message(self, cleaned_data):
        return "Comment was deleted"

    def get_success_url(self):
        return f"/projects/{self.request.POST['project_id']}#comments"

#-------------------------------------report----------------------------------------------#


def ReportProject(request, project_id):
    if request.method == 'POST':
        projectReports = ProjectReports(request.POST)
        if projectReports.is_valid():
            projectReports.save()
            messages.success(request, 'The report has sent successfully')
            return redirect('project', project_id=project_id)


def ReportComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    projectId = comment.project.id
    if request.method == 'POST':
        commentReports = CommentReport(request.POST)
        if commentReports.is_valid():
            commentReports.save()
            messages.success(request, 'The report has sent successfully')
            return redirect('project', project_id=projectId)

# -----------------------------------------rating--------------------------------


def submit_review(request, user_id, project_id):
    rate = ProjectRate.objects.filter(user=user_id, project=project_id).first()
    if request.method == 'POST':
        if rate:
            project_rate = ProjectRateForm(request.POST, instance=rate)
            if project_rate.is_valid():
                project_rate.save()
                messages.success(request, 'the rate has updated successfully')

        else:
            project_rate = ProjectRateForm(request.POST)
            project_rate.save()
            messages.success(request, 'the rate has sent successfully')
        return redirect('project', project_id=project_id)


def delete_rate(request, rate_id):
    rate = get_object_or_404(ProjectRate, id=rate_id)
    rate.delete()
    return redirect('project', project_id=rate.project.id)


@ csrf_exempt
def upload_project_images(request):

    try:
        for file in request.FILES.getlist('images'):
            my_file = file
            fs = FileSystemStorage("media/projects/images/")
            fs.save(my_file.name, my_file)

            print(f"projects/{my_file.name}")

        return JsonResponse({
            "message": "The images have been updated Successfully",
            "success": True
        })
    except BaseException as e:
        return JsonResponse({
            "message": "There is an error",
            "success": False
        })
        raise e


class ProjectViewSet(viewsets.ModelViewSet, APIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectImagesViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    serializer_class = ProjectImagesSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProjectImage.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
# -------------------Donation-----------------------------#


class CreateDonation(LoginRequiredMixin, CreateView):
    model = Donation
    template_name = 'projects/project.html'
    fields = ["donation_amount", "project"]

    def get_success_url(self):
        url = self.request.get_full_path()
        url = url.split("/")
        url.pop()
        url = "/".join(url)

        return url

    def form_valid(self, form):
        form.instance.donator_id = self.request.user.id
        return super(CreateDonation, self).form_valid(form)


def get_user_donations(request):
    donations = Donation.objects.filter(donator=request.user.id)
    context = {
        'donations': donations,
    }
    return render(request, 'projects/list_user_donation.html', context)

# ----------------Comment Reply----------------------#


class CreateCommentReply(SuccessMessageMixin, CreateView):
    model = CommentReply
    template_name = 'projects/project.html'
    fields = ["comment", "reply"]

    def get_success_url(self):
        return f"/projects/{self.request.POST['project']}#comment{self.kwargs['pk']}"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CreateCommentReply, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Comment Reply was Saved"
