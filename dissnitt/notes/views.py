from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Tag
from .forms import NoteForm, TagForm
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin



class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'notes/index.html'
    context_object_name = 'note_list'

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner__pk=user.id)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class TagFormView(SingleObjectMixin, generic.FormView):

    form_class = TagForm
    model = Tag

    def post(self, request, *args, **kwargs):
        form = request.POST
        tag_names = str(form['name']).split(" ")
        note = Note.objects.get(pk=kwargs['pk'])

        for n in tag_names:
            try:
                tag_obj = Tag.objects.get(name=n)

            except Tag.DoesNotExist:
                tag_obj = Tag(name=n)
                tag_obj.save()

            note.tags.add(tag_obj)

        return redirect('notes:detail', note.pk)

class NoteView(LoginRequiredMixin, generic.DetailView):

    model = Note
    template_name = 'notes/detail.html'

    def get_context_data(self, **kwargs):
        context = super(NoteView, self).get_context_data(**kwargs)
        context['form'] = TagForm
        context['tags'] = Tag.objects.all()
        return context


class DetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = NoteView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TagFormView.as_view()
        return view(request, *args, **kwargs)


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
    return redirect('notes:index')


class ByTagDetailView(LoginRequiredMixin, generic.DetailView):

    model = Tag
    template_name = 'notes/by_tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ByTagDetailView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context