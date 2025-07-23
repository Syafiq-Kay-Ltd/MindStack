# home/urls.py

from django.urls import path
from .views import ViewHomepage

urlpatterns = [
    path('', ViewHomepage, name='home'),
]