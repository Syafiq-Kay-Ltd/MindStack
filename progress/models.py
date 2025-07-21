from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class ProgressLog(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    summary = models.TextField(null=False, blank=False)
    details = models.TextField(null=False, blank=False)
    reflection = models.TextField(null=True, blank=True)
    next_action = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Progress Log'
        verbose_name_plural = 'Progress Logs'
        ordering = ['-creation_date']
        db_table = 'progress_log'

    def __str__(self):
        return self.title