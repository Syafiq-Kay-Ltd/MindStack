# cortexdb/views.py

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from cortexdb.forms import NoteForm
from cortexdb.models import Note


# CortexDB Main Page
class ViewMain(TemplateView):
    template_name = "cortexdb_main.html"

# CortexDB Notes CRUD
## CortexDB Notes CREATE
class ViewNotesCreate(FormView):
    template_name = "cortexdb_notes_create.html"
    form_class = NoteForm
    pk_url_kwarg = 'note_id'
    success_url = reverse_lazy('cortexdb:notes-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

## CortexDB Notes READ
### ... list
class ViewNotesList(ListView):
    model = Note
    template_name = "cortexdb_notes_list.html"

class ViewNotesDetail(DetailView):
    model = Note
    template_name = "cortexdb_notes_detail.html"

class ViewNotesUpdate(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'cortexdb_notes_create.html'
    success_url = reverse_lazy('cortexdb:notes-list')

class ViewNotesDelete(FormView):
    template_name = "cortexdb_notes_delete.html"
    success_url = reverse_lazy('cortexdb:notes-list')
    form_class = NoteForm

    def post(self, request, *args, **kwargs):
        note_id = self.kwargs.get('note_id')
        Note.objects.filter(id=note_id).delete()
        return super().post(request, *args, **kwargs)

