from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Tag
from .forms import NoteForm, TagForm
from django.views.generic.detail import SingleObjectMixin


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'notes/index.html'
    context_object_name = 'note_list'

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner__pk=user.id).order_by('created_date')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        context['tags'] = get_tags(user.id)
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
                tag_obj = Tag(name=n, owner=request.user)
                tag_obj.save()

            note.tags.add(tag_obj)

        return redirect('notes:detail', note.pk)

class NoteView(LoginRequiredMixin, generic.DetailView):

    model = Note
    template_name = 'notes/detail.html'

    def get_context_data(self, **kwargs):
        context = super(NoteView, self).get_context_data(**kwargs)
        user = self.request.user
        context['form'] = TagForm
        context['tags'] = get_tags(user.id)
        return context


class DetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = NoteView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TagFormView.as_view()
        return view(request, *args, **kwargs)


def get_notes(user_id):
    return Note.objects.filter(owner=user_id)

def get_tags(user_id):
    all_tags = Tag.objects.all().filter(owner=user_id).order_by('name')
    tags_w_count = [t for t in all_tags if t.note_set.all().count() > 0]
    return tags_w_count

@login_required
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

    user = request.user
    notes = get_notes(user.id)

    return render(request, 'notes/note_new.html', {'form': form, 'notes': notes})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:index')
    else:
        form = NoteForm(instance=note)

    user = request.user
    notes = get_notes(user.id)

    return render(request, 'notes/note_new.html', {'form': form, 'note': note, 'notes':notes})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('notes:index')


class ByTagDetailView(LoginRequiredMixin, generic.DetailView):

    model = Tag
    template_name = 'notes/by_tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ByTagDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        context['tags'] = get_tags(user.id)
        return context