# progress/views.py

from typing import Any
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import ModelFormMixin, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now

from progress.models import ProgressLog
from progress.forms import ProgressLogForm


# 📄 Main landing page
class ProgressMainPageView(TemplateView):
    template_name = "progress_mainpage.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["progresslog_list"] = ProgressLog.objects.all()
        context["progresslog"] = ProgressLog.objects.first()
        return context


# 📋 Log list
class ProgressLogListView(ListView):
    model = ProgressLog
    template_name = "progress_log_list.html"
    context_object_name = "progresslog_list"


# 🔎 Individual log view
class ProgressLogDetailView(DetailView):
    model = ProgressLog
    template_name = "progress_log_detail.html"
    context_object_name = "progresslog"


# 🆕 Create a new log
class ProgressLogCreateView(CreateView):
    model = ProgressLog
    form_class = ProgressLogForm
    template_name = "progress_log_form.html"

    def form_valid(self, form):
        log = form.save(commit=False)
        log.creator = self.request.user
        log.creation_date = now()
        log.save()
        return redirect("progress:progress-log-detail", pk=log.pk)


# 📝 Edit existing log
class ProgressLogUpdateView(UpdateView):
    model = ProgressLog
    form_class = ProgressLogForm
    template_name = "progress_log_form.html"

    def get_queryset(self):
        return ProgressLog.objects.filter(creator=self.request.user)

    def get_success_url(self):
        return reverse("progress:progress-log-detail", kwargs={"pk": self.object.pk})


# ❌ Delete log
class ProgressLogDeleteView(DeleteView):
    model = ProgressLog
    template_name = "progress_log_confirm_delete.html"
    success_url = reverse_lazy("progress:progress-log-list")


# 🧪 Optional: Unified form view (create/edit via ?id=)
class ProgressLogFormView(ModelFormMixin, FormView):
    model = ProgressLog
    form_class = ProgressLogForm
    template_name = "progress_log_form.html"

    def get_object(self):
        id = self.request.GET.get("id")
        if id:
            return ProgressLog.objects.filter(id=id, creator=self.request.user).first()
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_object()
        if instance:
            kwargs["instance"] = instance
        return kwargs

    def form_valid(self, form):
        log = form.save(commit=False)
        log.creator = self.request.user
        if not log.pk:
            log.creation_date = now()
        log.save()
        return redirect("progress:progress-log-detail", pk=log.pk)
