import pytest
from django.urls import reverse
from home.models import TemplateTokenLog
from django.test import TestCase

class TestHomepageView(TestCase):
    def test_homepage_renders_with_token(self):
        # Request the homepage view
        response = self.client.get(reverse('home'))
        # Check the response is OK
        self.assertEqual(response.status_code, 200)
        # Check the token is in the context
        self.assertIn('template_token', response.context)
        token = response.context['template_token']
        # Check the token is rendered in the HTML
        self.assertIn(token, response.content.decode())
        # Check the token exists in the database
        self.assertTrue(TemplateTokenLog.objects.filter(template_name='home.html', token=token).exists())
        # Ensure only one token exists for this template
        self.assertEqual(TemplateTokenLog.objects.filter(template_name='home.html').count(), 1)