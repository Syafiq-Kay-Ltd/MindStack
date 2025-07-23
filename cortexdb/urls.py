# cortexdb/urls.py

from django.urls import path
from .views_crud import (
    CortexDBIndexView,
    ViewCortexDBNotes,
    ViewCortexDBNotesCreate,
    ViewCortexDBNotesUpdate,
)

app_name = 'cortexdb'
urlpatterns = [
    path('', CortexDBIndexView, name='index'),
    path('notes/', ViewCortexDBNotes.as_view(), name='notes-list'),
    path('notes/create/', ViewCortexDBNotesCreate.as_view(), name='notes-create'),
    path('notes/update/<int:note_id>/', ViewCortexDBNotesUpdate.as_view(), name='notes-update'),
]