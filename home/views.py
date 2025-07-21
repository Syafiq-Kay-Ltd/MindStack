# home/views.py

from django.views.generic import TemplateView

class HomeView(TemplateView):
    """
    Home view that renders the home page.
    """
    template_name = 'home.html'
