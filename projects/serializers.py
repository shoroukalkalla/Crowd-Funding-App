from rest_framework import serializers

from .models import Project, ProjectImage

class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
       model = Project
       fields = '__all__'


class ProjectImagesSerializer(serializers.ModelSerializer):
   class Meta:
       model = ProjectImage
       fields = '__all__'
       