from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_date = models.DateTimeField('date created')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title