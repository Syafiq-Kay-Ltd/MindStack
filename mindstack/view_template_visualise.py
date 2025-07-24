import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
from django.urls import get_resolver
from django.test import Client
import graphviz

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindstack.settings')
django.setup()

from django.conf import settings

def get_view_template_map():
    """
    Recursively returns a mapping of view names to the templates they render by following all URL patterns, including those from include().
    """
    from django.urls.resolvers import URLPattern, URLResolver
    resolver = get_resolver()
    client = Client()
    view_template_map = {}

    def follow_patterns(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                if hasattr(pattern, 'name') and pattern.name:
                    try:
                        url = prefix + str(pattern.pattern)
                        url = url.replace('<int:id>', '1').replace('<int:pk>', '1').replace('<slug:slug>', 'test-slug')
                        url = '/' + url if not url.startswith('/') else url
                        response = client.get(url)
                        templates = [t.name for t in getattr(response, 'templates', []) if t.name]
                        view_template_map[pattern.name] = templates
                    except Exception as e:
                        view_template_map[pattern.name] = [f'Error: {e}']
            elif isinstance(pattern, URLResolver):
                # Recursively follow included patterns
                follow_patterns(pattern.url_patterns, prefix + str(pattern.pattern))

    follow_patterns(resolver.url_patterns)
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
