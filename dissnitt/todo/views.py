from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Task, SubTask
from .forms import ProjectForm, TaskForm, SubTaskForm
from django.utils import timezone


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'todo/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner__pk=user.pk).order_by('priority')


class DetailView(LoginRequiredMixin, generic.DetailView):

    model = Project
    template_name = 'todo/detail.html'

@login_required
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.completed = False
            project.created_date = timezone.now()
            project.save()
            return redirect('todo:index')

    else:
        form = ProjectForm()

    return render(request, 'todo/project_new.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project.save()
            return redirect('todo:index')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'todo/project_edit.html', {'form': form, 'project':project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()

    return redirect('todo:index')

@login_required
def new_task(request, pk):
    project_id = get_object_or_404(Project, pk=pk)
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project_id
            task.completed = False
            task.created_date = timezone.now()
            task.save()
            return redirect('todo:detail', project.pk)
    else:
        form = TaskForm()

    return render(request, 'todo/task_new.html', {'form':form, 'project':project})

@login_required
def edit_task(request, pk, tk):
    task = get_object_or_404(Task, pk=tk)
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            return redirect('todo:detail', pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/task_edit.html', {'form': form, 'project':project, 'task':task})

@login_required
def delete_task(request, pk, tk):
    task = get_object_or_404(Task, pk=tk)
    task.delete()
    return redirect('todo:detail', pk)

@login_required
def new_subtask(request, pk, tk):
    task_id = get_object_or_404(Task, pk=tk)
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subt = form.save(commit=False)
            subt.task = task_id
            subt.completed = False
            subt.created_date = timezone.now()
            subt.save()
            return redirect('todo:detail', pk)
    else:
        form = SubTaskForm()

    return render(request, 'todo/subtask_edit.html', {'form':form, 'task':task_id, 'project':project})

@login_required
def edit_subtask(request, pk, sk):
    subtask = get_object_or_404(SubTask, pk=sk)
    task_id = subtask.task
    # task = Task.objects.get(pk=task_id)
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            subtask.save()
            return redirect('todo:detail', pk)
    else:
        form = SubTaskForm(instance=subtask)

    return render(request, 'todo/subtask_edit.html', {'form':form, 'task':task_id, 'project':project})

@login_required
def delete_subtask(request, pk, sk):
    subtask = get_object_or_404(SubTask, pk=sk)
    subtask.delete()
    return redirect('todo:detail', pk)
