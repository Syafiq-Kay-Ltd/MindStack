import pytest
from django.test import TestCase
from .models import note

class TestCortexDBURLS(TestCase):
    pass

@pytest.mark.django_db
class TestCortexDBViews(TestCase):
    pass

@pytest.mark.django_db
class TestNoteModelsCRUD(TestCase):
    
    def test_can_create_note(self):
        first = note.objects.create(title="note just created")
        first.save()
        assert note.objects.filter(title="note just created").exists()

    def test_can_read_note(self):
        second = note.objects.create(title="note to be read")
        second.save()
        assert note.objects.filter(title="note to be read").exists()
        assert second.note_id is not None
        assert second.content == ""
    
    def test_can_update_note(self):
        third = note.objects.create(title="note to be edited")
        assert third is not None
        third.title = "note that has been edited"
        third.save()
        assert note.objects.filter(title="note that has been edited")
        assert not note.objects.filter(title="note to be edited")

    def test_can_delete_note(self):
        fourth = note.objects.create(title="note to be deleted")
        assert note.objects.filter(title="note to be deleted").exists()
        fourth.delete()
        assert not note.objects.filter(title="note to be deleted").exists()
