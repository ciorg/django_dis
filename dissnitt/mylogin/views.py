from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notes.models import Tag, Note
from todo.models import Project


@login_required(login_url='/mylogin/login/')
def home(request):
    user = request.user
    projects = Project.objects.filter(owner__pk=user.pk)
    cprojects = projects.filter(owner__pk=user.pk).filter(completed=True)

    try:
        cperc = round((float(len(cprojects))/float(len(projects)))*100, 2)

    except ZeroDivisionError:
        cperc = 0.00

    notes = Note.objects.filter(owner__pk=user.pk)
    tags = Tag.objects.filter(owner__pk=user.pk)

    context = {
        'projects':projects,
        'cprojects': cprojects,
        'cperc': cperc,
        'notes': notes,
        'tags': tags
    }

    return render(request, 'mylogin/home.html', context)
