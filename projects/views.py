from django.shortcuts import render


from .forms import ProjectForm, ProjectImageForm, TagForm
from .models import ProjectImage,Tag

# Create your views here.


def get_projects(request):
    return render(request, 'projects/projects.html')


def get_project(request, project_id):
    return render(request, 'projects/project.html')


def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        # Adding New Tags 
        retags = request.POST.getlist('tags[]')
        for tag in retags:
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create( name=tag, is_verified= False )
        #Creating new Project
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save() 
            for tag in retags:
                project.tags.add(Tag.objects.get(name=tag))
            project.save()
            
       
          
    project_form = ProjectForm()
    verifiedTags = Tag.objects.filter(is_verified = True)
    context = {'project_form': project_form, 'tags' : verifiedTags}

    return render(request, "projects/project_create.html", context)
