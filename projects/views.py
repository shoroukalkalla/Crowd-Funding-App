from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ProjectForm
from .models import Comment, ProjectImage, Tag, Project, Donation
from users.models import User

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
    comments=Comment.objects.filter(project_id=project_id)    
    data = {'project': project, 'user': user, 'images': images, "num_of_Projects": num_of_Projects, 'donation_amount': amount['donation_amount__sum'], 'donators':donators ,'comments':comments}
    return data



def get_projects(request):
    project_array = []

    projects = Project.objects.all().values('id')
    for project in projects:
        data = get_project_data(project['id'])
        project_array.append(data)

    for p in project_array:
        print(p)
        print("\n================================")

    return render(request, 'projects/projects.html', {'projects':project_array})


def get_project(request, project_id):
    context = get_project_data(project_id)     
    return render(request, 'projects/project.html', context)


def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        # fetching Images
        images = request.FILES.getlist('images')
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
                ProjectImage.objects.create(image=img, project=project)

        return redirect('project', project_id=project.id)

    project_form = ProjectForm()
    verifiedTags = Tag.objects.filter(is_verified=True)
    context = {'project_form': project_form, 'tags': verifiedTags}

    return render(request, "projects/project_create.html", context)


# -------------------------------------------------------------#

# def add_comment(request):
#     if request.method =="POST":
#         form=Comment(request.POST , request.FILES)
#         if form.is_valid():
#             comment = form.save()
#             return redirect("project" , project_id=comment.project_id)
#     else:
#         form = Comment()
#     return render(request , "pro/form.html" , context={"form": form})    


class CreateComment(CreateView):
    model = Comment
    template_name = 'projects/create_comment.html'
    fields = "__all__"
    success_url = reverse_lazy('project')

class EditComment(UpdateView):
    model = Comment
    template_name = 'projects/create_comment.html'
    queryset = Comment.objects.all()
    fields = ["comment", "user_id" ,"project_id"]
    # success_url = reverse_lazy('projects')
    success_url = "/"

    def get_queryset(self):
        print("##########Query##########################")
        return super().get_queryset()
    print("#####################")
    def form_valid(self, form ):
        print("#####################")
        print(self.request)
        print("#####################")
        return super().form_valid(form)


class DeleteComment(DeleteView):
    model = Comment
    pk_ur_kwargs = 'comment.id'
    template_name = 'projects/delete_comment.html'
    success_url = reverse_lazy('projects')    