# progress/urls.py
from django.urls import path
from .views import ProgressMainPageView

app_name = 'progress'
urlpatterns = [
    path('', ProgressMainPageView.as_view(), name='progress-main'),
]
