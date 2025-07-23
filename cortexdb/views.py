# cortexdb/views.py

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from .forms import NoteForm
from .models import Note
from .services import get_note_context

# CortexDB Main Page
class ViewMain(TemplateView):
    template_name = "cortexdb_main.html"

# CortexDB Notes CRUD
## CortexDB Notes CREATE
class ViewNotesCreate(FormView):
    form_class = NoteForm
    template_name = "cortexdb_notes_create.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'cortexdb:notes-detail', 
            kwargs={
                'note_id': self.object.pk
            }
        )

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

