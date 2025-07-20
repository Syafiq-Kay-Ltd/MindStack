import pytest
from django.urls import reverse
from django.urls.resolvers import Resolver404, get_resolver

# test that pytest is working
def test_pytest_works():
    assert True

# test progress-mainpage renders correctly
# Constant for the progress main URL name
PROGRESS_MAIN_URL_NAME = 'progress:progress-main'
# test progress-mainpage renders correctly
def test_progress_main_renders(client):
    response = client.get(reverse(PROGRESS_MAIN_URL_NAME))
    assert response.status_code == 200

# test that the URL resolver can resolve the progress main URL
def test_progress_main_url_resolves():
    resolver = get_resolver()
    try:
        resolver.resolve(reverse(PROGRESS_MAIN_URL_NAME))
    except Resolver404:
        pytest.fail(f"URL '{PROGRESS_MAIN_URL_NAME}' could not be resolved.")
    else:
        assert True, f"URL '{PROGRESS_MAIN_URL_NAME}' resolved successfully."

