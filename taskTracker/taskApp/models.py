from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    pwd = models.CharField(max_length=100)
    profileUrl = models.CharField(max_length=200, default="")
    lastLoggedIn = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Project(models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=200, null=True, blank=True)
    repo = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_members')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    isAdmin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

class List(models.Model):
    name = models.CharField(max_length=100, default="unnamed list")
    order = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='lists')

class Issue(models.Model):
    order = models.IntegerField()
    priority = models.IntegerField()
    type = models.IntegerField()
    summary = models.CharField(max_length=100)
    descr = models.CharField(max_length=500, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')

class Assignee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_issues')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='assignees')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_assignees')
    createdAt = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    descr = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_comments')
