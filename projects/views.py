from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProjectForm
from .models import Comment, ProjectImage, Tag, Project, Donation
from users.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here.


def get_project_data(project_id):
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=project.user.id)
    images = ProjectImage.objects.filter(project_id=project.id)
    num_of_Projects = user.project_set.count()
    amount = Donation.objects.filter(
        project_id=project.id).aggregate(Sum('donation_amount'))
    donators = Donation.objects.filter(
        project_id=project.id).values('donator').distinct().count()
    comments = Comment.objects.filter(project_id=project_id)
    data = {'project': project, 'user': user, 'images': images, "num_of_Projects": num_of_Projects,
            'donation_amount': amount['donation_amount__sum'], 'donators': donators, 'comments': comments}
    return data


def get_projects(request):
    project_array = []

    projects = Project.objects.all().values('id')
    for project in projects:
        data = get_project_data(project['id'])
        project_array.append(data)

    return render(request, 'projects/projects.html', {'projects': project_array})


def get_project(request, project_id):
    context = get_project_data(project_id)
    return render(request, 'projects/project.html', context)


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


# -------------------------------------------------------------#


class CreateComment(CreateView):
    model = Comment
    template_name = 'projects/create_comment.html'
    fields = ["comment", "project"]

    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CreateComment, self).form_valid(form)


class EditComment(UpdateView):
    model = Comment
    template_name = 'projects/create_comment.html'
    fields = ["comment", "project"]
    pk_ur_kwargs = 'comment.id'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(EditComment, self).form_valid(form)


class DeleteComment(DeleteView):
    model = Comment
    pk_ur_kwargs = 'comment.id'
    template_name = 'projects/delete_comment.html'
    success_url = reverse_lazy('projects')


@csrf_exempt
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
