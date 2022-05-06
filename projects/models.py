from django.db import models
from users.models import User

from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    is_verified = models.fieldName = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=150)
    details = models.CharField(max_length=150)
    total_target = models.IntegerField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_opened = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/images",
                              height_field=None, width_field=None, max_length=100)


class Dontation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    donator = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_amount = models.IntegerField()


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)


class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.CharField(max_length=150)


class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.CharField(max_length=150)


class ProjectRate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
