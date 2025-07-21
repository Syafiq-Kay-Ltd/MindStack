import pytest
from django.test import TestCase
from cortexdb.models import Note

@pytest.mark.django_db
class TestCreateNotes(TestCase):
    def test_create_note(self):
        # Create a test note
        note = Note.objects.create(
            title="Test Note",
            content="This is a test note"
        )
        
        # Assertions to verify the note was created correctly
        assert note.title == "Test Note"
        assert note.content == "This is a test note"
        assert note.note_id is not None
        assert note.created_at is not None
        assert note.updated_at is not None