# cortexdb/views.py

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from cortexdb.forms import NoteForm
from cortexdb.models import Note

class CortexDBIndexView(TemplateView):
    template_name = "cortexdb_index.html"

# CortexDB Notes - CRUD Views
class ViewCortexDBNotesCreate(FormView):
    template_name = "cortexdb_notes_create.html"
    form_class = NoteForm
    success_url = "/cortexdb/notes/"

    def form_valid(self, form):
        note = form.save()
        return super().form_valid(form)

class ViewCortexDBNotes(TemplateView):
    template_name = "cortexdb_notes.html"

class ViewCortexDBNotesUpdate(FormView):
    template_name = "cortexdb_notes_update.html"
    form_class = NoteForm
    success_url = "/cortexdb/notes/"

    def get_initial(self):
        note_id = self.kwargs.get('note_id')
        note = Note.objects.get(note_id=note_id)
        return {
            'title': note.title,
            'content': note.content
        }

    def form_valid(self, form):
        note = form.save(commit=False)
        note.note_id = self.kwargs.get('note_id')
        note.save()
        return super().form_valid(form)

class ViewCortexDBNotesDelete(FormView):
    template_name = "cortexdb_notes_delete.html"
    success_url = "/cortexdb/notes/"

    def post(self, request, *args, **kwargs):
        note_id = self.kwargs.get('note_id')
        Note.objects.filter(note_id=note_id).delete()
        return super().post(request, *args, **kwargs)