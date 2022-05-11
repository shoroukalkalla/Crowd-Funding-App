from datetime import datetime
from importlib.metadata import files
from statistics import mode
from tracemalloc import start
from .models import Project, Category, Tag, ProjectImage,ProjectReport,CommentReport,ProjectRate
from django import forms
from django.forms.widgets import DateTimeInput, DateInput


class ProjectForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", ],
        widget=DateTimeInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'))
    end_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", ],
        widget=DateTimeInput(format='%Y-%m-%dT%H:%M',
        attrs={'type': 'datetime-local', 'min': datetime.now().date()}))

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
            'details': forms.Textarea(attrs={'cols': 200, 'rows': 5}),

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


class ProjectReports(forms.ModelForm):
    class Meta:
        model =ProjectReport
        fields = '__all__'

class CommentReport(forms.ModelForm):
    class Meta:
        model =CommentReport
        fields = '__all__'

class ProjectRateForm(forms.ModelForm):
    class Meta:
        model =ProjectRate
        fields = '__all__'