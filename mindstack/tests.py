import pytest

@pytest.mark.django_db
@pytest.mark.xfail(reason="admin configuration is not set up yet")
def test_admin_configuration():
    """
    Test that the Django admin configuration is set up correctly.
    """
    from django.contrib.admin.sites import site
    assert site.is_registered('auth.User'), "User model should be registered in admin."
    assert site.is_registered('auth.Group'), "Group model should be registered in admin."
    assert site.is_registered('progress.Progress'), "Progress model should be registered in admin."
    assert site.is_registered('progress.Task'), "Task model should be registered in admin."

@pytest.mark.xfail(reason="admin access is not configured yet")
def test_admin_accessible(client):
    """
    Test that the Django admin interface is accessible.
    """
    response = client.get('/admin/')
    assert response.status_code == 200, "Admin interface should be accessible."