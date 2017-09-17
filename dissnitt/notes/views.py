from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Tag
from .forms import NoteForm, TagForm


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'notes/index.html'
    context_object_name = 'note_list'

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner__pk=user.id)


class DetailView(LoginRequiredMixin, generic.DetailView):

    model = Note
    template_name = 'notes/detail.html'


def new_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.created_date = timezone.now()
            note.save()
            return redirect('notes:index')

    else:
        form = NoteForm()

    return render(request, 'notes/note_new.html', {'form': form})

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:index')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_new.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect(request, 'notes:index' )
