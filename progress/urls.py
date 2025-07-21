# progress/urls.py

from django.urls import path
from .views import (
    ProgressMainPageView,
    ProgressLogListView,
    ProgressLogDetailView,
    ProgressLogCreateView,
    ProgressLogUpdateView,
    ProgressLogDeleteView,
    ProgressLogFormView,  # Optional unified create/edit view
)

app_name = "progress"

urlpatterns = [
    # 🔖 Landing & overview
    path("", ProgressMainPageView.as_view(), name="progress-main"),
    path("logs/", ProgressLogListView.as_view(), name="progress-log-list"),

    # 📄 Individual log access
    path("log/<int:pk>/", ProgressLogDetailView.as_view(), name="progress-log-detail"),

    # ✏️ Form endpoints
    path("log/new/", ProgressLogCreateView.as_view(), name="progress-log-create"),
    path("log/<int:pk>/edit/", ProgressLogUpdateView.as_view(), name="progress-log-update"),
    path("log/form/", ProgressLogFormView.as_view(), name="progress-log-form"),  # Accepts ?id=123 for edit

    # ❌ Log deletion
    path("log/<int:pk>/delete/", ProgressLogDeleteView.as_view(), name="progress-log-delete"),
]
