# home/views.py
from django.views.generic import TemplateView

class ViewHomepage(TemplateView):
    template_name = 'home.html'
    