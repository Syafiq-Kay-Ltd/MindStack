from django.test import TestCase, Client
from django.urls import resolve
from home.models import TemplateTokenLog
import re

class TestViewTemplateTokenLogging(TestCase):
    def log_template_token(self, view_url):
        """
        Follows the view at view_url, finds the HTML template used, and logs the token from the rendered HTML.
        """
        client = Client()
        response = client.get(view_url)
        self.assertEqual(response.status_code, 200)
        # Find token in HTML comment
        match = re.search(r'<!-- TOKEN: ([a-f0-9]{64}) -->', response.content.decode())
        self.assertIsNotNone(match, f"No token found in HTML for {view_url}")
        token = match.group(1)
        # Find template name from response (if available)
        template_name = None
        if hasattr(response, 'templates') and response.templates:
            template_name = response.templates[0].name
        else:
            # Fallback: try to guess from URL
            template_name = view_url.strip('/').split('/')[-1] + '.html'
        # Log token in the database
        obj, created = TemplateTokenLog.objects.get_or_create(template_name=template_name)
        obj.token = token
        obj.save()
        return template_name, token

    def test_home_view_token_logging(self):
        template_name, token = self.log_template_token('/')
        self.assertTrue(TemplateTokenLog.objects.filter(template_name=template_name, token=token).exists())
