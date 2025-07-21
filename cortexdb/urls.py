# cortexdb/urls.py

from django.urls import path
from . import views

app_name = 'cortexdb'
urlpatterns = [
    path('', views.CortexDBIndexView.as_view(), name='index'),
]