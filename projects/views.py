from django.shortcuts import render


# Create your views here.


def get_projects(request):
    return render(request, 'projects/projects.html')


def get_project(request, project_id):
    return render(request, 'projects/project.html')


