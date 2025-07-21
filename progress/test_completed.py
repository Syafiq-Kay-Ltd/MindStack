import pytest
from django.urls import reverse
from django.urls.resolvers import Resolver404, get_resolver

# test that pytest is working
def test_pytest_works():
    assert True

# test progress-mainpage renders correctly
# Constant for the progress main URL name
@pytest.mark.django_db
class TestProgressLogInitialisation:
    PROGRESS_MAIN_URL_NAME = 'progress:progress-main'

    def test_progress_main_renders(self, client):
        response = client.get(reverse(self.PROGRESS_MAIN_URL_NAME))
        assert response.status_code == 200

    # test that the URL resolver can resolve the progress main URL
    def test_progress_main_url_resolves(self):
        resolver = get_resolver()
        try:
            resolver.resolve(reverse(self.PROGRESS_MAIN_URL_NAME))
        except Resolver404:
            pytest.fail(f"URL '{self.PROGRESS_MAIN_URL_NAME}' could not be resolved.")
        else:
            assert True, f"URL '{self.PROGRESS_MAIN_URL_NAME}' resolved successfully."

