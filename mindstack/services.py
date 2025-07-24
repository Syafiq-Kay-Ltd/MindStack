import hashlib
import time

def generate_template_token(template_name: str) -> str:
    """
    Generates a unique token for a given template name using the current timestamp and a hash.
    """
    timestamp = str(int(time.time()))
    raw = f"{template_name}:{timestamp}"
    token = hashlib.sha256(raw.encode()).hexdigest()
    return token
def get_or_create_template_token(template_name: str) -> str:
    """
    Returns a single token for the given template name. If not present, generates and stores it.
    This ensures only one token exists per template (tokenisation phase).
    """
    from home.models import TemplateTokenLog
    obj, created = TemplateTokenLog.objects.get_or_create(template_name=template_name)
    if created or not obj.token:
        import hashlib, time
        timestamp = str(int(time.time()))
        raw = f"{template_name}:{timestamp}"
        obj.token = hashlib.sha256(raw.encode()).hexdigest()
        obj.save()
    return obj.token
"""
Service functions for the mindstack app.

Manual:
- generate_template_token(template_name: str) -> str
    Generates a unique token for a given template name and logs it in the database (TemplateTokenLog).

    Example usage scenarios:
    1. In a Django view to log template usage:
        from mindstack.services import generate_template_token
        def my_view(request):
            token = generate_template_token('my_template.html')
            return render(request, 'my_template.html')

    2. In a test to verify token logging:
        from mindstack.services import generate_template_token
        from home.models import TemplateTokenLog
        def test_token_logging():
            token = generate_template_token('test_template.html')
            assert TemplateTokenLog.objects.filter(token=token).exists()

    3. For auditing template usage in admin or scripts:
        from home.models import TemplateTokenLog
        logs = TemplateTokenLog.objects.filter(template_name='progress_base.html')
        for log in logs:
            print(log.token, log.created_at)

    4. In a management command to clean up old tokens:
        from home.models import TemplateTokenLog
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=30)
        TemplateTokenLog.objects.filter(created_at__lt=cutoff).delete()

    5. In a signal to automatically log template usage when a view is called:
        from django.dispatch import receiver
        from django.core.signals import request_finished
        from mindstack.services import generate_template_token
        @receiver(request_finished)
        def log_template_token(sender, **kwargs):
            generate_template_token('some_template.html')
"""
import hashlib
