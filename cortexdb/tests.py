import pytest
from django.test import TestCase
from django.urls import reverse, NoReverseMatch, resolve
from .models import Note
from cortexdb import views

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
        self.check_view('cortexdb:notes-create', 'cortexdb_notes_form.html')

    def test_notes_list_view(self):
        self.check_view('cortexdb:notes-list', 'cortexdb_notes_list.html')

    def test_notes_detail_view(self):
        self.check_view('cortexdb:notes-detail', 'cortexdb_notes_detail.html', kwargs={'pk': self.note.pk})

    def test_notes_update_view(self):
        self.check_view('cortexdb:notes-update', 'cortexdb_notes_form.html', kwargs={'pk': self.note.pk})

    def test_notes_update_does_not_create_new_entry(self):
        # Count notes before update
        initial_count = Note.objects.count()
        # Update the note via POST
        response = self.client.post(reverse('cortexdb:notes-update', kwargs={'pk': self.note.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content.'
        })
        self.assertEqual(response.status_code, 302)
        # Count notes after update
        after_count = Note.objects.count()
        # Should not create a new entry
        self.assertEqual(initial_count, after_count)
        # The note should be updated
        updated_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(updated_note.title, 'Updated Title')
        self.assertEqual(updated_note.content, 'Updated content.')

    def test_notes_delete_view(self):
        self.check_view('cortexdb:notes-delete', 'cortexdb_notes_delete.html', kwargs={'pk': self.note.pk})

    # Test Note creation via POST
    def test_note_creation_form_submission(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Created via test',
            'content': 'This is a test note body.',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Note.objects.filter(title='Created via test').exists())

    # Test Note deletion via POST
    def test_note_deletion_form_submission(self):
        pk = self.note.pk
        delete_url = reverse('cortexdb:notes-delete', kwargs={'pk': pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful deletion
        self.assertFalse(Note.objects.filter(pk=pk).exists())  # Confirm note was deleted

# URLS
class TestCortexDBURLS(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='Sample', content='Test content.')

    def test_notes_list_url_resolves(self):
        url = reverse('cortexdb:notes-list')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.ViewNotesList)

    def test_notes_create_url_resolves(self):
        url = reverse('cortexdb:notes-create')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.ViewNotesCreate)

    def test_notes_detail_url_resolves(self):
        url = reverse('cortexdb:notes-detail', kwargs={'pk': self.note.pk})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.ViewNotesDetail)

    def test_notes_update_url_resolves(self):
        url = reverse('cortexdb:notes-update', kwargs={'pk': self.note.pk})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.ViewNotesUpdate)

    def test_notes_delete_url_resolves(self):
        url = reverse('cortexdb:notes-delete', kwargs={'pk': self.note.pk})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.ViewNotesDelete)


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

class NoteWorkflowTest(TestCase):
    def test_full_note_lifecycle(self):
        # Step 1: Create a new note
        create_url = reverse('cortexdb:notes-create')
        response = self.client.post(create_url, {
            'title': 'Workflow Test Note',
            'content': 'This content is part of a lifecycle test.'
        })
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(title='Workflow Test Note')
        pk = note.pk

        # Step 2: View the note
        detail_url = reverse('cortexdb:notes-detail', kwargs={'pk': pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workflow Test Note')

        # Step 3: Update the note
        update_url = reverse('cortexdb:notes-update', kwargs={'pk': pk})
        response = self.client.post(update_url, {
            'title': 'Updated Note Title',
            'content': 'Updated content.'
        })
        self.assertEqual(response.status_code, 302)
        updated_note = Note.objects.get(pk=pk)
        self.assertEqual(updated_note.title, 'Updated Note Title')

        # Step 4: Delete the note
        delete_url = reverse('cortexdb:notes-delete', kwargs={'pk': pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=pk).exists())

class TechSavvyUserTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='Savvy Note', content='Smart input')

    def test_can_access_note_detail(self):
        url = reverse('cortexdb:notes-detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_can_access_note_update(self):
        url = reverse('cortexdb:notes-update', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_can_access_note_delete(self):
        url = reverse('cortexdb:notes-delete', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TechNaiveUserTests(TestCase):
    def test_typo_in_update_url(self):
        response = self.client.get('/cortexdb/notes/updat/1/')
        self.assertEqual(response.status_code, 404)

    def test_missing_trailing_slash(self):
        response = self.client.get('/cortexdb/notes/detail/1')
        self.assertIn(response.status_code, [301, 404])  # Redirect or not found based on APPEND_SLASH

    def test_access_list_without_slash(self):
        response = self.client.get('/cortexdb/notes')
        self.assertIn(response.status_code, [301, 404])

class MaliciousActorTests(TestCase):
    def test_sql_injection_like_pk(self):
        response = self.client.get('/cortexdb/notes/detail/1%20OR%201=1/')
        self.assertEqual(response.status_code, 404)

    def test_non_integer_pk(self):
        response = self.client.get('/cortexdb/notes/detail/abc/')
        self.assertEqual(response.status_code, 404)

    def test_post_to_readonly_detail_view(self):
        note = Note.objects.create(title='Malicious', content='Probe')
        url = reverse('cortexdb:notes-detail', kwargs={'pk': note.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)  # Method not allowed
    
    def test_reverse_with_non_integer_pk(self):
        with self.assertRaises(NoReverseMatch):
            reverse('cortexdb:notes-detail', kwargs={'pk': 'abc'})

class URLReverseResilienceTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='Resilient', content='Robust routing')

    def test_named_routes_reverse_correctly(self):
        routes = [
            ('cortexdb:notes-list', {}),
            ('cortexdb:notes-create', {}),
            ('cortexdb:notes-detail', {'pk': self.note.pk}),
            ('cortexdb:notes-update', {'pk': self.note.pk}),
            ('cortexdb:notes-delete', {'pk': self.note.pk}),
        ]
        for name, kwargs in routes:
            url = reverse(name, kwargs=kwargs)
            self.assertTrue(url.startswith('/cortexdb/notes'))

@pytest.mark.xfail(reason="Archiving functionality not implemented")
class ArchiveNoteTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='To archive', content='Legacy note')

    def test_note_can_be_archived(self):
        response = self.client.post(reverse('cortexdb:notes-archive', kwargs={'pk': self.note.pk}))
        self.note.refresh_from_db()
        self.assertTrue(self.note.is_archived)

@pytest.mark.xfail(reason="Search functionality not implemented")
class SearchNoteTests(TestCase):
    def setUp(self):
        Note.objects.create(title='AI tools', content='Copilot is powerful.')
        Note.objects.create(title='Gardening', content='Soil composition matters.')

    def test_search_notes_by_keyword(self):
        response = self.client.get(reverse('cortexdb:notes-search'), {'q': 'copilot'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI tools')
        self.assertNotContains(response, 'Gardening')

@pytest.mark.xfail(reason="Tagging feature not available yet")
class TagNoteTests(TestCase):
    def test_create_note_with_tags(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Tagged Note',
            'content': 'This note has tags.',
            'tags': 'django,testing,modularity'
        })
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(title='Tagged Note')
        self.assertEqual(note.tags.count(), 3)

@pytest.mark.xfail(reason="Title case validation not enforced yet")
class TitleValidationTests(TestCase):
    def test_title_not_title_case_should_fail(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'this is lowercase',
            'content': 'Valid content.'
        })
        self.assertEqual(response.status_code, 200)  # Expecting form to re-render due to validation error
        self.assertContains(response, "Title must be in title case")

@pytest.mark.xfail(reason="Content sanitization not implemented yet")
class ContentValidationTests(TestCase):
    def test_content_with_disallowed_characters_should_fail(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Valid Title',
            'content': 'This content includes illegal characters like @#^~`'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content contains unsupported characters")

@pytest.mark.xfail(reason="Validation logic not yet in place")
class ValidNoteSubmissionTests(TestCase):
    def test_valid_title_and_content_should_pass(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Proper Title Case',
            'content': 'This is clean content with accepted symbols like £ $ % - !'
        })
        self.assertEqual(response.status_code, 302)
        from cortexdb.models import Note
        self.assertTrue(Note.objects.filter(title='Proper Title Case').exists())

@pytest.mark.xfail(reason="Tag model and note-tag relationship not implemented")
class TagModelTests(TestCase):
    def test_can_assign_tags_to_note(self):
        response = self.client.post(reverse('cortexdb:notes-create'), {
            'title': 'Tagged Note',
            'content': 'Note with tags.',
            'tags': 'python,zettelkasten,workflow'
        })
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(title='Tagged Note')
        self.assertEqual(note.tags.count(), 3)

    def test_can_filter_notes_by_tag(self):
        response = self.client.get(reverse('cortexdb:notes-filter-by-tag', kwargs={'slug': 'zettelkasten'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tagged Note')

@pytest.mark.xfail(reason="Note linking via backlinks not supported yet")
class NoteLinkingTests(TestCase):
    def test_can_link_notes_together(self):
        parent = Note.objects.create(title='Parent Note', content='Seed idea.')
        child = Note.objects.create(title='Linked Note', content='Related expansion.')

        response = self.client.post(reverse('cortexdb:notes-link'), {
            'source_id': parent.pk,
            'target_id': child.pk,
            'relation_type': 'related'
        })
        self.assertEqual(response.status_code, 302)
        assert child in parent.linked_notes.all()

@pytest.mark.xfail(reason="Note review tracking not implemented")
class NoteProcessingTests(TestCase):
    def test_review_counter_increments(self):
        note = Note.objects.create(title='Review Note', content='Reviewable.')
        response = self.client.post(reverse('cortexdb:notes-review', kwargs={'pk': note.pk}))
        note.refresh_from_db()
        self.assertEqual(note.review_count, 1)

    def test_paraphrase_logged(self):
        note = Note.objects.create(title='Original', content='Some idea.')
        response = self.client.post(reverse('cortexdb:notes-paraphrase', kwargs={'pk': note.pk}), {
            'content': 'Reworded version for clarity.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(note.paraphrases.count(), 1)

@pytest.mark.xfail(reason="Note splitting logic not yet implemented")
class SplitNoteTests(TestCase):
    def test_split_creates_multiple_child_notes(self):
        note = Note.objects.create(title='Composite Note', content='1. First idea. 2. Second idea.')
        response = self.client.post(reverse('cortexdb:notes-split', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 302)
        assert Note.objects.filter(parent_id=note.pk).count() == 2

@pytest.mark.xfail(reason="Note merging not yet supported")
class MergeNoteTests(TestCase):
    def test_merge_combines_note_content(self):
        a = Note.objects.create(title='Note A', content='Intro.')
        b = Note.objects.create(title='Note B', content='Details.')
        response = self.client.post(reverse('cortexdb:notes-merge'), {
            'source_ids': [a.pk, b.pk],
            'merged_title': 'Combined Note'
        })
        self.assertEqual(response.status_code, 302)
        assert Note.objects.filter(title='Combined Note').exists()

@pytest.mark.xfail(reason="Optimisation engine not yet implemented")
class ZettelkastenOptimisationTests(TestCase):
    def test_can_suggest_notes_to_link(self):
        note = Note.objects.create(title='Atomic Note', content='Idea that overlaps.')
        response = self.client.get(reverse('cortexdb:notes-suggestions', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Potential link')

    def test_can_list_orphan_notes(self):
        response = self.client.get(reverse('cortexdb:notes-orphans'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unlinked')

@pytest.mark.xfail(reason="Mindmap view and rendering not implemented yet")
class MindmapViewTests(TestCase):
    def setUp(self):
        self.parent = Note.objects.create(title='Atomic Note A', content='Core idea A.')
        self.child = Note.objects.create(title='Atomic Note B', content='Related idea B.')
        # Simulate a link with future Link model
        self.link_description = "builds on concept of causality"

    def test_mindmap_view_renders_nodes(self):
        response = self.client.get(reverse('cortexdb:notes-mindmap'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Atomic Note A')
        self.assertContains(response, 'Atomic Note B')

    def test_mindmap_truncates_content_to_10_words(self):
        long_note = Note.objects.create(title='Long Note', content=' '.join(f'word{i}' for i in range(25)))
        response = self.client.get(reverse('cortexdb:notes-mindmap'))
        self.assertEqual(response.status_code, 200)
        rendered_card = response.content.decode()
        assert len(rendered_card.split()) <= 20  # 10 words title + 10 words body max

    def test_mindmap_shows_link_label_between_notes(self):
        # Future: associate notes via Link table and display link label
        response = self.client.get(reverse('cortexdb:notes-mindmap'))
        self.assertContains(response, self.link_description)

import pytest
from django.test import TestCase
from cortexdb.models import Note, Tag, Link, Processing, SplitGroup, MergeRecord

# ------------------------------
# 📝 Note CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="Note model or form validation not fully implemented")
class NoteCRUDTests(TestCase):
    def test_create_note(self):
        note = Note.objects.create(title='Test', content='Sample')
        self.assertEqual(note.title, 'Test')

    def test_read_note(self):
        note = Note.objects.create(title='Readable', content='Visible content')
        fetched = Note.objects.get(pk=note.pk)
        self.assertEqual(fetched.content, 'Visible content')

    def test_update_note(self):
        note = Note.objects.create(title='Initial', content='Version 1')
        note.title = 'Updated'
        note.save()
        self.assertEqual(Note.objects.get(pk=note.pk).title, 'Updated')

    def test_delete_note(self):
        note = Note.objects.create(title='Delete Me', content='To be removed')
        pk = note.pk
        note.delete()
        self.assertFalse(Note.objects.filter(pk=pk).exists())

# ------------------------------
# 🏷 Tag CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="Tag model or note-tag M2M link not implemented")
class TagCRUDTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name='python')
        self.assertEqual(tag.name, 'python')

    def test_read_tag(self):
        tag = Tag.objects.create(name='research')
        self.assertEqual(Tag.objects.get(name='research').name, 'research')

    def test_update_tag(self):
        tag = Tag.objects.create(name='oldname')
        tag.name = 'newname'
        tag.save()
        self.assertEqual(Tag.objects.get(pk=tag.pk).name, 'newname')

    def test_delete_tag(self):
        tag = Tag.objects.create(name='temp')
        pk = tag.pk
        tag.delete()
        self.assertFalse(Tag.objects.filter(pk=pk).exists())

    def test_assign_tag_to_note(self):
        note = Note.objects.create(title='Tagged', content='Tag me')
        tag = Tag.objects.create(name='zettel')
        tag.notes.add(note)
        self.assertIn(note, tag.notes.all())

# ------------------------------
# 🔗 Link CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="Link model or note relations not defined")
class LinkCRUDTests(TestCase):
    def test_create_link(self):
        a = Note.objects.create(title='A', content='...')
        b = Note.objects.create(title='B', content='...')
        link = Link.objects.create(source=a, target=b, description='Contextual connection')
        self.assertEqual(link.description, 'Contextual connection')

    def test_read_link(self):
        a = Note.objects.create(title='A', content='...')
        b = Note.objects.create(title='B', content='...')
        link = Link.objects.create(source=a, target=b, description='test')
        self.assertEqual(Link.objects.get(pk=link.pk).source.title, 'A')

    def test_update_link_description(self):
        a = Note.objects.create(title='A', content='...')
        b = Note.objects.create(title='B', content='...')
        link = Link.objects.create(source=a, target=b, description='Initial')
        link.description = 'Revised'
        link.save()
        self.assertEqual(Link.objects.get(pk=link.pk).description, 'Revised')

    def test_delete_link(self):
        a = Note.objects.create(title='X', content='...')
        b = Note.objects.create(title='Y', content='...')
        link = Link.objects.create(source=a, target=b, description='Disposable')
        pk = link.pk
        link.delete()
        self.assertFalse(Link.objects.filter(pk=pk).exists())

# ------------------------------
# 📈 Processing CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="Processing model not integrated with note lifecycle")
class ProcessingCRUDTests(TestCase):
    def test_create_processing_record(self):
        note = Note.objects.create(title='Tracked', content='...')
        proc = Processing.objects.create(note=note, reviewed_count=1)
        self.assertEqual(proc.reviewed_count, 1)

    def test_read_processing(self):
        note = Note.objects.create(title='History', content='...')
        proc = Processing.objects.create(note=note, paraphrased_count=2)
        self.assertEqual(Processing.objects.get(pk=proc.pk).paraphrased_count, 2)

    def test_update_processing(self):
        note = Note.objects.create(title='Metrics', content='...')
        proc = Processing.objects.create(note=note)
        proc.reviewed_count += 3
        proc.save()
        self.assertEqual(Processing.objects.get(pk=proc.pk).reviewed_count, 3)

    def test_delete_processing(self):
        note = Note.objects.create(title='Temp', content='...')
        proc = Processing.objects.create(note=note)
        pk = proc.pk
        proc.delete()
        self.assertFalse(Processing.objects.filter(pk=pk).exists())

# ------------------------------
# ✂️ SplitGroup CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="SplitGroup logic not yet tied to split workflows")
class SplitGroupCRUDTests(TestCase):
    def test_create_split_group(self):
        original = Note.objects.create(title='Parent', content='Compound idea')
        child1 = Note.objects.create(title='A', content='Part A')
        child2 = Note.objects.create(title='B', content='Part B')
        group = SplitGroup.objects.create(original_note=original)
        group.child_notes.set([child1, child2])
        self.assertEqual(group.child_notes.count(), 2)

    def test_read_split_group(self):
        original = Note.objects.create(title='X', content='...')
        group = SplitGroup.objects.create(original_note=original)
        self.assertEqual(group.original_note.title, 'X')

    def test_delete_split_group(self):
        original = Note.objects.create(title='Z', content='...')
        group = SplitGroup.objects.create(original_note=original)
        pk = group.pk
        group.delete()
        self.assertFalse(SplitGroup.objects.filter(pk=pk).exists())

# ------------------------------
# 🔀 MergeRecord CRUD Tests
# ------------------------------
@pytest.mark.xfail(reason="MergeRecord not integrated with merge logic")
class MergeRecordCRUDTests(TestCase):
    def test_create_merge_record(self):
        a = Note.objects.create(title='Note A', content='...')
        b = Note.objects.create(title='Note B', content='...')
        merged = MergeRecord.objects.create(title='Merged AB')
        merged.notes.set([a, b])
        self.assertEqual(merged.notes.count(), 2)

    def test_read_merge_record(self):
        merged = MergeRecord.objects.create(title='Combined')
        self.assertEqual(MergeRecord.objects.get(pk=merged.pk).title, 'Combined')

    def test_update_merge_title(self):
        merged = MergeRecord.objects.create(title='Old Title')
        merged.title = 'New Title'
        merged.save()
        self.assertEqual(MergeRecord.objects.get(pk=merged.pk).title, 'New Title')

    def test_delete_merge_record(self):
        record = MergeRecord.objects.create(title='Temp Merge')
        pk = record.pk
        record.delete()
        self.assertFalse(MergeRecord.objects.filter(pk=pk).exists())
