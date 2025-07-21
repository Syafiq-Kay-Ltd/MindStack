# cortexdb/views.py

from django.views.generic import TemplateView

class CortexDBIndexView(TemplateView):
    template_name = "cortexdb_index.html"