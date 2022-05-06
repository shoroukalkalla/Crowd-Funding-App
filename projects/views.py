from django.shortcuts import render


from .forms import ProjectForm
from .models import ProjectImage,Tag

# Create your views here.


def get_projects(request):
    return render(request, 'projects/projects.html')


def get_project(request, project_id):
    return render(request, 'projects/project.html')


def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        #fetching Images
        images = request.FILES.getlist('images')
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
            #saving tages 
            for tag in retags:
                project.tags.add(Tag.objects.get(name=tag))
            project.save()
            #saving images
            for img in images:
                ProjectImage.objects.create(image=img, project=project)

            
       
          
    project_form = ProjectForm()
    verifiedTags = Tag.objects.filter(is_verified = True)
    context = {'project_form': project_form, 'tags' : verifiedTags}

    return render(request, "projects/project_create.html", context)
