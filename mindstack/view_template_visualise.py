import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
from django.urls import get_resolver
from django.test import Client
import graphviz

# Setup Django environment

# Use production settings and ensure read-only mode
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindstack.settings')
django.setup()

# Set DB to read-only if possible (for SQL Server, this is best done at the DB level)
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SET TRANSACTION ISOLATION LEVEL SNAPSHOT;")
except Exception as e:
    print(f"Could not set DB to read-only mode: {e}")

from django.conf import settings

def get_view_template_map():
    # Create dummy objects for views that require pk
    from cortexdb.models import Note  # Adjust model name if needed
    try:
        dummy_note, created = Note.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'Dummy Note',
                'content': 'Dummy content',
                # Add other required fields here
            }
        )
    except Exception as e:
        print(f"Could not create dummy note: {e}")
    """
    Recursively returns a mapping of view names to the templates they render by following all URL patterns, including those from include().
    """
    from django.urls.resolvers import URLPattern, URLResolver
    import importlib
    client = Client()
    view_template_map = {}
    cortexdb_urls = importlib.import_module('cortexdb.urls')
    patterns = getattr(cortexdb_urls, 'urlpatterns', [])

    def follow_patterns(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                if hasattr(pattern, 'name') and pattern.name:
                    try:
                        url = prefix + str(pattern.pattern)
                        # Replace all Django path converters with dummy values
                        url = url.replace('<int:id>', '1').replace('<int:pk>', '1').replace('<slug:slug>', 'test-slug')
                        url = url.replace('<str:pk>', '1').replace('<uuid:pk>', '00000000-0000-0000-0000-000000000000')
                        url = url.replace('<str:id>', '1').replace('<uuid:id>', '00000000-0000-0000-0000-000000000000')
                        import re
                        url = re.sub(r'<[^>]+>', '1', url)
                        url = '/' + url if not url.startswith('/') else url
                        response = client.get(url)
                        templates = [t.name for t in getattr(response, 'templates', []) if t.name]
                        if templates:
                            view_template_map[pattern.name] = templates
                        else:
                            view_template_map[pattern.name] = ['No template rendered']
                    except Exception as e:
                        view_template_map[pattern.name] = [f'Error: {e}']
            elif isinstance(pattern, URLResolver):
                follow_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

    follow_patterns(patterns)
    return view_template_map

def visualise_view_template_map(view_template_map, output_file='view_template_map.gv'):
    dot = graphviz.Digraph(comment='View-Template Mapping')
    for view, templates in view_template_map.items():
        dot.node(view, view, shape='box', style='filled', color='lightblue')
        for template in templates:
            dot.node(template, template, shape='ellipse', style='filled', color='lightgrey')
            dot.edge(view, template)
    dot.render(output_file, view=True)
    print(f'Graph saved to {output_file}')

if __name__ == '__main__':
    view_template_map = get_view_template_map()
    visualise_view_template_map(view_template_map)
