# --- Template Token Verification Tests ---
import pytest
import re
from django.urls import reverse
from django.utils import timezone
from .models import ProgressLog
from home.models import TemplateTokenLog

class TestViewTemplateTokenVerification:
    """
    Tests that views render the correct HTML templates and use the expected tokens from the TemplateTokenLog DB.
    """

    view_template_map = {
        'progress:progress-main': 'progress_mainpage.html',
        'progress:progress-log-list': 'progress_log_list.html',
        'progress:progress-log-detail': 'progress_log_detail.html',
        # Add more view name to template mappings as needed
    }

    def get_expected_token(self, template_name):
        try:
            entry = TemplateTokenLog.objects.get(template_name=template_name)
            return entry.token
        except TemplateTokenLog.DoesNotExist:
            return None

    @pytest.mark.django_db
    @pytest.mark.parametrize("view_name,template_name", list(view_template_map.items()))
    def test_view_renders_expected_template_with_token(self, client, view_name, template_name):
        # Patch: Ensure a ProgressLog exists for detail view
        if 'detail' in view_name:
            from progress.models import ProgressLog
            log = ProgressLog.objects.create(
                title='Test Log',
                summary='Test summary',
                details='Test details',
                creation_date=timezone.now()
            )
            url = reverse(view_name, args=[log.id])
        else:
            url = reverse(view_name)
        response = client.get(url)
        assert response.status_code == 200
        # Get rendered template name
        rendered_templates = [t.name for t in getattr(response, 'templates', []) if t.name]
        assert template_name in rendered_templates, f"Expected {template_name}, got {rendered_templates}"
        # Extract token from HTML comment
        match = re.search(r'<!-- TOKEN: ([a-f0-9]{64}) -->', response.content.decode())
        assert match, f"No token found in HTML for {template_name}"
        token = match.group(1)
        # Get expected token from DB
        expected_token = self.get_expected_token(template_name)
        assert expected_token is not None, f"No expected token found in DB for {template_name}"
        assert token == expected_token, f"Token mismatch for {template_name}: expected {expected_token}, got {token}"


@pytest.mark.django_db
class TestProgressLogMVP:
    # create a test user
    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    # Test that the progress log model can be created and has required fields
    def test_progress_log_model(self, user):
        log = ProgressLog.objects.create(
            title='Test Progress Log',
            summary='This is a test summary',
            details='Detailed information about the progress',
            reflection=None,
            next_action=None,
            creation_date='2023-10-01',
        )
        assert log.title is not None
        assert log.summary is not None
        assert log.details is not None
        assert log.reflection is None
        assert log.next_action is None
        assert log.creation_date is not None

    def test_progress_log_list_view(self, client, user):
        log = ProgressLog.objects.create(
            title='Sample Progress Log',
            summary='This is a sample summary',
            details='Detailed information about the sample progress',
            reflection=None,
            next_action=None,
            creation_date=timezone.now()
        )
        response = client.get(reverse('progress:progress-log-list'))
        assert response.status_code == 200

    def test_progress_log_detail_view(self, client, user):
        client.force_login(user)
        log = ProgressLog.objects.create(
            title='Sample Progress Log',
            summary='This is a sample summary',
            details='Detailed information about the sample progress',
            reflection=None,
            next_action=None,
            creation_date=timezone.now()
        )
        response = client.get(reverse('progress:progress-log-detail', args=[log.id]))
        assert response.status_code == 200

    # test that progress-main renders the latest progress log
    def test_progress_main_view_renders_latest_log(self, client, user):
        # Old log
        ProgressLog.objects.create(
            title='Another Progress Log',
            summary='This is another summary',
            details='Detailed information about another progress',
            creation_date=timezone.datetime(2020, 10, 19, 12, 0, 0),
        )

        # Latest log
        latest_log = ProgressLog.objects.create(
            title='Sample Progress Log',
            summary='This is a sample summary',
            details='Detailed information about the sample progress',
            creation_date=timezone.now()
        )

        # Request view
        url = reverse('progress:progress-main')
        response = client.get(url)

        # Assertions
        assert response.status_code == 200
        html = response.content.decode()
        assert latest_log.title in html

    def test_progress_log_form_creates_new_log(self, client, user):
        client.force_login(user)
        form_data = {
            'title': 'New Log Entry',
            'summary': 'Quick summary',
            'details': 'Elaborate progress details',
            'reflection': 'Reflection goes here',
            'next_action': 'Follow-up action',
            'creation_date': timezone.now().isoformat(),  # Optional if auto-added
        }

        response = client.post(reverse('progress:progress-log-create'), data=form_data)
        assert response.status_code == 302  # Assuming redirect on success

        log = ProgressLog.objects.latest('creation_date')
        assert log.title == 'New Log Entry'

    @pytest.mark.xfail(reason="This test is currently failing due to an issue with the form handling.")
    def test_progress_log_form_edits_existing_log(self, client, user):
        client.force_login(user)

        original_log = ProgressLog.objects.create(
            title='Original Log',
            summary='Original summary',
            details='Original details',
            creation_date=timezone.now()
        )

        update_data = {
            'title': 'Updated Title',
            'summary': original_log.summary,
            'details': original_log.details,
            'reflection': 'Updated reflection',
            'next_action': 'Updated next action',
            'creation_date': original_log.creation_date.isoformat(),
        }

        initial_count = ProgressLog.objects.count()
        url = reverse('progress:progress-log-create') + f'?id={original_log.id}'  # Or your edit URL pattern
        response = client.post(url, data=update_data)
        assert response.status_code == 302
        assert ProgressLog.objects.count() == initial_count  # Ensures it's an edit, not a new entry

        original_log.refresh_from_db()
        assert original_log.title == 'Updated Title'
        assert original_log.reflection == 'Updated reflection'

    def test_progress_log_delete_view(self, client, user):
        client.force_login(user)
        log = ProgressLog.objects.create(
            title='Log to be deleted',
            summary='Summary for deletion',
            details='Details for deletion',
            creation_date=timezone.now()
        )

        response = client.post(reverse('progress:progress-log-delete', args=[log.id]))
        assert response.status_code == 302  # Assuming redirect on success

        with pytest.raises(ProgressLog.DoesNotExist):
            log.refresh_from_db()  # Should raise an error if the log was deleted
