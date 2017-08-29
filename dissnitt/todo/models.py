from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=30)
    created_date = models.DateTimeField('created_date')
    completed = models.BooleanField()
    description = models.TextField()
    priority = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_name = models.CharField(max_length=30)
    created_date = models.DateTimeField('created_date')
    completed = models.BooleanField()
    description = models.TextField()
    priority = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name

class SubTask(models.Model):
    sub_name = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name