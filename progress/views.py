# progress/views.py
from typing import Any
from django.views.generic import TemplateView, ListView, DetailView
from progress.models import ProgressLog

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