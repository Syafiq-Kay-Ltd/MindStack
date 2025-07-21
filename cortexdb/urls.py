# cortexdb/urls.py

from django.urls import path
from . import views

app_name = 'cortexdb'
urlpatterns = [
    path('', views.CortexDBIndexView.as_view(), name='index'),
    path('notes/', views.ViewCortexDBNotes.as_view(), name='notes-list'),
    path('notes/create/', views.ViewCortexDBNotesCreate.as_view(), name='notes-create'),
    path('notes/update/<int:note_id>/', views.ViewCortexDBNotesUpdate.as_view(), name='notes-update'),
]