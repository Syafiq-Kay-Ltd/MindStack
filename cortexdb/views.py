# cortexdb/views.py

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from .forms import NoteForm
from .models import Note
from .services import get_note_context

class NoteFormMixin:
    model = Note
    form_class = NoteForm
    template_name = 'cortexdb_notes_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = 'edit' if self.object else 'create'
        return context

# CortexDB Main Page
class ViewMain(TemplateView):
    template_name = "cortexdb_main.html"

# CortexDB Notes CRUD
## CortexDB Notes CREATE
class ViewNotesCreate(NoteFormMixin, CreateView):
    success_url = reverse_lazy('cortexdb:notes-list')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    

## CortexDB Notes READ
### ... list
class ViewNotesList(ListView):
    model = Note
    template_name = "cortexdb_notes_list.html"
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_context = get_note_context(self.request, context['notes'])
        context.update(service_context)
        return context

### ... details
class ViewNotesDetail(DetailView):
    model = Note
    template_name = "cortexdb_notes_detail.html"

## UPDATE
class ViewNotesUpdate(NoteFormMixin, UpdateView):
    success_url = reverse_lazy('cortexdb:notes-list')

    def form_valid(self, form):
        # Add custom logic here
        return super().form_valid(form)

## DELETE
class ViewNotesDelete(DeleteView):
    model = Note
    template_name = "cortexdb_notes_delete.html"
    success_url = reverse_lazy('cortexdb:notes-list')
