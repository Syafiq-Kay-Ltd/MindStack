# progress/urls.py
from django.urls import path
from .views import (
    ProgressMainPageView,
    ProgressLogListView,
    ProgressLogDetailView,
    ProgressLogCreateView,
    ProgressLogUpdateView,
    ProgressLogDeleteView,
)

app_name = 'progress'
urlpatterns = [
    path('', ProgressMainPageView.as_view(), name='progress-main'),
    path('progress-log/', ProgressLogListView.as_view(), name='progress-log-list'),
    path('log/<int:pk>/', ProgressLogDetailView.as_view(), name='progress-log-detail'),
    path('log/create/', ProgressLogCreateView.as_view(), name='progress-log-create'),
    path('log/<int:pk>/update/', ProgressLogUpdateView.as_view(), name='progress-log-update'),
    path('log/<int:pk>/delete/', ProgressLogDeleteView.as_view(), name='progress-log-delete'),
]
