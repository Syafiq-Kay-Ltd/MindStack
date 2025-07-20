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