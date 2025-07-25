from django.db import models

# model for project category: cat_id (PK), title, description

# model for project: project_id (PK), cat_id (FK), title, description, created_at, updated_at, status

# model for tag: probably links to cortexdb tag model TBC

class TemplateTokenLog(models.Model):
    template_name = models.CharField(max_length=255)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template_name} - {self.token}"
