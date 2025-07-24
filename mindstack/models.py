from django.db import models

class TemplateTokenLog(models.Model):
    template_name = models.CharField(max_length=255)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template_name} - {self.token}"
