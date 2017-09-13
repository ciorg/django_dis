from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_date = models.DateTimeField('date created')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
