# progress/views.py
from django.views.generic import TemplateView

class ProgressMainPageView(TemplateView):
    template_name = "progress_mainpage.html"
