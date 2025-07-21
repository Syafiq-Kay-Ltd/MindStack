# progress/tests.py

import pytest
from django.urls import reverse
from django.utils import timezone
from .models import ProgressLog
@pytest.mark.django_db
class TestProgressLogMVP():
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
        from progress.models import ProgressLog
        log = ProgressLog.objects.create(
            creator=user,
            title='Test Progress Log',
            summary='This is a test summary',
            details='Detailed information about the progress',
            reflection=None,
            next_action=None,
            creation_date='2023-10-01',
        )
        assert log.creator.id == 1
        assert log.title is not None
        assert log.summary is not None
        assert log.details is not None
        assert log.reflection is None
        assert log.next_action is None
        assert log.creation_date is not None

    def test_progress_log_list_view(self, client, user):
        log = ProgressLog.objects.create(
            creator=user,
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
            creator=user,
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
            creator=user,
            title='Another Progress Log',
            summary='This is another summary',
            details='Detailed information about another progress',
            creation_date=timezone.datetime(2020, 10, 19, 12, 0, 0),
        )

        # Latest log
        latest_log = ProgressLog.objects.create(
            creator=user,
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

        response = client.post(reverse('progress:progress-log-form'), data=form_data)
        assert response.status_code == 302  # Assuming redirect on success

        log = ProgressLog.objects.latest('creation_date')
        assert log.creator == user
        assert log.title == 'New Log Entry'
    
    def test_progress_log_form_edits_existing_log(self, client, user):
        client.force_login(user)
        original_log = ProgressLog.objects.create(
            creator=user,
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

        url = reverse('progress:progress-log-form') + f'?id={original_log.id}'  # Or your edit URL pattern
        response = client.post(url, data=update_data)
        assert response.status_code == 302

        original_log.refresh_from_db()
        assert original_log.title == 'Updated Title'
        assert original_log.reflection == 'Updated reflection'
    
    def test_progress_log_delete_view(self, client, user):
        client.force_login(user)
        log = ProgressLog.objects.create(
            creator=user,
            title='Log to be deleted',
            summary='Summary for deletion',
            details='Details for deletion',
            creation_date=timezone.now()
        )

        response = client.post(reverse('progress:progress-log-delete', args=[log.id]))
        assert response.status_code == 302  # Assuming redirect on success

        with pytest.raises(ProgressLog.DoesNotExist):
            log.refresh_from_db()  # Should raise an error if the log was deleted