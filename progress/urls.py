# progress/urls.py
from django.urls import path
from .views import (
    ProgressMainPageView,
    ProgressLogListView,
    ProgressLogDetailView
)

app_name = 'progress'
urlpatterns = [
    path('', ProgressMainPageView.as_view(), name='progress-main'),
    path('progress-log/', ProgressLogListView.as_view(), name='progress-log-list'),
    path('log/<int:pk>/', ProgressLogDetailView.as_view(), name='progress-log-detail'),
]
