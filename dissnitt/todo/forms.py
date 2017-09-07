from django import forms
from .models import Project, Task, SubTask


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'priority', 'completed']

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['task_name', 'description', 'completed', 'priority']

class SubTaskForm(forms.ModelForm):

    class Meta:
        model = SubTask
        fields = ['sub_name']