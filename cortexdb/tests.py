import pytest
from django.test import TestCase
from django.urls import reverse
from cortexdb.models import Note
from cortexdb.views import ViewMain

# VIEWS
@pytest.mark.django_db
class CortexdbViewsTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Test Note")

    def check_view(self, url_name, expected_template, kwargs=None):
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template)

    def test_main_view(self):
        self.check_view('cortexdb:main', 'cortexdb_main.html')

    def test_notes_create_view(self):
        self.check_view('cortexdb:notes-create', 'cortexdb_notes_create.html')

    def test_notes_list_view(self):
        self.check_view('cortexdb:notes-list', 'cortexdb_notes_list.html')

    def test_notes_detail_view(self):
        self.check_view('cortexdb:notes-detail', 'cortexdb_notes_detail.html', kwargs={'pk': self.note.pk})

    def test_notes_update_view(self):
        self.check_view('cortexdb:notes-update', 'cortexdb_notes_create.html', kwargs={'pk': self.note.pk})

    def test_notes_delete_view(self):
        self.check_view('cortexdb:notes-delete', 'cortexdb_notes_delete.html', kwargs={'note_id': self.note.pk})

    # Test Note creation via POST
    def test_note_creation_form_submission(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Created via test',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Note.objects.filter(title='Created via test').exists())

    # Test Note deletion via POST
    def test_note_deletion_form_submission(self):
        pk = self.note.pk
        response = self.client.post(reverse('cortexdb:notes-delete', kwargs={'note_id': pk}))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertFalse(Note.objects.filter(pk=pk).exists())

# URLS
class TestCortexDBURLS(TestCase):
    pass

# MODEL - Note - CRUD
@pytest.mark.django_db
class TestNoteModelsCRUD(TestCase):
    # CREATE
    def test_can_create_Note(self):
        first = Note.objects.create(title="Note just created")
        first.save()
        assert Note.objects.filter(title="Note just created").exists()

    # READ
    def test_can_read_Note(self):
        second = Note.objects.create(title="Note to be read")
        second.save()
        assert Note.objects.filter(title="Note to be read").exists()
        assert second.note_id is not None
        assert second.content == ""
    
    # UPDATE
    def test_can_update_Note(self):
        third = Note.objects.create(title="Note to be edited")
        assert third is not None
        third.title = "Note that has been edited"
        third.save()
        assert Note.objects.filter(title="Note that has been edited")
        assert not Note.objects.filter(title="Note to be edited")

    # DELETE
    def test_can_delete_Note(self):
        fourth = Note.objects.create(title="Note to be deleted")
        assert Note.objects.filter(title="Note to be deleted").exists()
        fourth.delete()
        assert not Note.objects.filter(title="Note to be deleted").exists()
