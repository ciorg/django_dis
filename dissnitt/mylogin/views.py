from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notes.models import Tag, Note
from todo.models import Project


@login_required(login_url='/mylogin/login/')
def home(request):
    projects = Project.objects.all()
    cprojects = projects.filter(completed=True)
    cperc = round((float(len(cprojects))/float(len(projects)))*100, 2)
    notes = Note.objects.all()
    tags = Tag.objects.all()

    context = {
        'projects':projects,
        'cprojects': cprojects,
        'cperc': cperc,
        'notes': notes,
        'tags': tags
    }

    return render(request, 'mylogin/home.html', context)
