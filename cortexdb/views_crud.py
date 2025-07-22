# cortexdb/views_crud.py

from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from cortexdb.forms import NoteForm
from cortexdb.models import Note
from django.shortcuts import render 

# CortexDB Landing Page
def CortexDBIndexView(request):
    return render(
        request,
        'cortexdb_index.html',
        {
            'context': 'context'
        }
    )

# Notes
class ViewCortexDBNotesCreate(FormView):
    template_name = "cortexdb_notes_create.html"
    form_class = NoteForm
    success_url = "/cortexdb/notes/"

    def form_valid(self, form):
        note = form.save()
        return super().form_valid(form)

class ViewCortexDBNotes(TemplateView):
    template_name = "cortexdb_notes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.all()
        return context

class ViewCortexDBNotesUpdate(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'cortexdb/note_form.html'
    success_url = reverse_lazy('cortexdb:notes-list')
    pk_url_kwarg = 'note_id'

class ViewCortexDBNotesDelete(FormView):
    template_name = "cortexdb_notes_delete.html"
    success_url = "/cortexdb/notes/"

    def post(self, request, *args, **kwargs):
        note_id = self.kwargs.get('note_id')
        Note.objects.filter(note_id=note_id).delete()
        return super().post(request, *args, **kwargs)
