# progress/views.py
from typing import Any
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from progress.models import ProgressLog
from django.urls import reverse_lazy

class ProgressMainPageView(TemplateView):
    template_name = "progress_mainpage.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        progresslog = ProgressLog.objects.first()
        if not progresslog:
            context["progresslog"] = None
            context["progresslog_list"] = ProgressLog.objects.all()
        else:
            context["progresslog"] = progresslog
        return context
    

class ProgressLogListView(ListView):
    model = ProgressLog
    template_name = "progress_log_list.html"

class ProgressLogDetailView(DetailView):
    model = ProgressLog
    template_name = "progress_log_detail.html"

class ProgressLogCreateView(CreateView):
    model = ProgressLog
    template_name = "progress_log_form.html"
    fields = ['title', 'summary', 'details', 'reflection', 'next_action', 'creation_date']
    
    def get_success_url(self):
        return reverse_lazy('progress:progress-log-detail', kwargs={'pk': self.object.pk})

class ProgressLogUpdateView(UpdateView):
    model = ProgressLog
    template_name = "progress_log_form.html"
    fields = ['title', 'summary', 'details', 'reflection', 'next_action', 'creation_date']
    def get_success_url(self):
        return reverse_lazy('progress:progress-log-detail', kwargs={'pk': self.object.pk})

class ProgressLogDeleteView(DeleteView):
    model = ProgressLog
    template_name = "progress_log_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy('progress:progress-log-list')