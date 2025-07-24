# home/mixins.py

class TemplateTokenMixin:
    def get_template_token(self):
        """
        Returns a single token for the given template name. If not present, generates and stores it.
        This ensures only one token exists per template (tokenisation phase).
        """
        from home.models import TemplateTokenLog
        import hashlib, time
        obj, created = TemplateTokenLog.objects.get_or_create(template_name=self.template_name)
        if created or not obj.token:
            timestamp = str(int(time.time()))
            raw = f"{self.template_name}:{timestamp}"
            obj.token = hashlib.sha256(raw.encode()).hexdigest()
            obj.save()
        return obj.token

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a single token for this template to the context
        context['template_token'] = self.get_template_token()
        return context
