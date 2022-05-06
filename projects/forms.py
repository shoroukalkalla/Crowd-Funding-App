
from tracemalloc import start
from .models import Project, Category, Tag, ProjectImage
from django import forms
from django.forms.widgets import DateTimeInput, DateInput
from .widgets import XDSoftDateTimePickerInput



class ProjectForm(forms.ModelForm):
    start_time = forms.DateTimeField(
    widget=DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_time = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Project
        fields = [
            "title",
            "details",
            "category",
            "total_target",
            "start_time",
            "end_time",
        ]
        widgets = {
             'details': forms.Textarea(attrs={'cols': 200, 'rows': 5 }),
           
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = '__all__'
