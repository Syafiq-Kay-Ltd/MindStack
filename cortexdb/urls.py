# cortexdb/urls.py

from django.urls import path
from .views import (
    ViewMain, ViewNotesCreate, ViewNotesList, ViewNotesDetail, ViewNotesUpdate, ViewNotesDelete
)

app_name = 'cortexdb'
urlpatterns = [
    # main
    path('', ViewMain.as_view(), name='main'),
    # notes CRUD
    ## notes CREATE
    path('notes/create/', ViewNotesCreate.as_view(), name='notes-create'),
    ## notes READ
    path('notes/', ViewNotesList.as_view(), name='notes-list'),
    path('notes/<int:note_id>', ViewNotesDetail.as_view(), name='notes-detail'),
    ## notes UPDATE
    path('notes/update/<int:note_id>/', ViewNotesUpdate.as_view(), name='notes-update'),
    ## notes DELETE
    path('notes/delete/<int:note_id>', ViewNotesDelete.as_view(), name='notes-delete')
]