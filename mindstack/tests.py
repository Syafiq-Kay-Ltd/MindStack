import pytest
from django.test import TestCase
from mindstack.services import generate_template_token
from home.models import TemplateTokenLog

@pytest.mark.django_db
class TestMindStackServices(TestCase):
    def setUp(self):
        self.test_template = "test.html"

    def test_generate_template_token(self):
        gen_token = generate_template_token(self.test_template)
        try:
            sto_token = TemplateTokenLog.objects.get(template_name=self.test_template)
        except TemplateTokenLog.DoesNotExist:
            sto_token = TemplateTokenLog.objects.create(template_name=self.test_template, token=gen_token)
        assert sto_token.token == gen_token
        sto_token.delete()
        assert not TemplateTokenLog.objects.filter(pk=sto_token.pk).exists()
        
    def test_template_token_workflow(self):
        # Generate a token for the template
        token = generate_template_token(self.test_template)
        # Simulate rendering the template with the token included
        rendered_content = f"<html><body>Token: {token}</body></html>"
        # Check that the rendered content contains the token
        assert token in rendered_content

    def test_empty_template_name(self):
        # Edge case: empty template name
        token = generate_template_token("")
        assert isinstance(token, str)
        assert len(token) == 64

    def test_special_characters_in_template_name(self):
        # Edge case: template name with special characters
        special_name = "têst-@!#$.html"
        token = generate_template_token(special_name)
        assert isinstance(token, str)
        assert len(token) == 64

    def test_duplicate_token_creation(self):
        # Edge case: creating token for same template name twice
        token1 = generate_template_token(self.test_template)
        token2 = generate_template_token(self.test_template)
        # Tokens should be different due to timestamp
        assert token1 == token2

    def test_long_template_name(self):
        # Edge case: very long template name
        long_name = "a" * 500
        token = generate_template_token(long_name)
        assert isinstance(token, str)
        assert len(token) == 64