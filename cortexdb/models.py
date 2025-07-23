from django.db import models

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

class Tag(models.Model):
    # placeholder only
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Link(models.Model):
    # placeholder relationships
    source = models.ForeignKey('Note', related_name='outgoing_links', on_delete=models.CASCADE)
    target = models.ForeignKey('Note', related_name='incoming_links', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.source} → {self.target}"


class Processing(models.Model):
    # placeholder fields
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    reviewed_count = models.PositiveIntegerField(default=0)
    paraphrased_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Processing: {self.note.title}"


class SplitGroup(models.Model):
    # placeholder relationships
    original_note = models.ForeignKey('Note', related_name='split_origin', on_delete=models.CASCADE)
    child_notes = models.ManyToManyField('Note', related_name='split_children')

    def __str__(self):
        return f"SplitGroup: {self.original_note.title}"


class MergeRecord(models.Model):
    # placeholder relationships
    title = models.CharField(max_length=255)
    notes = models.ManyToManyField('Note', related_name='merged_into')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merge: {self.title}"
