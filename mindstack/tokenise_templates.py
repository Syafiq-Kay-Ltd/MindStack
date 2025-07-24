import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import hashlib
import django
import re

# Always use test settings for DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindstack.settings')
os.environ['DJANGO_TEST_DB'] = '1'
django.setup()

from home.models import TemplateTokenLog

def generate_token(template_name):
    raw = f"{template_name}:{os.urandom(16).hex()}"
    return hashlib.sha256(raw.encode()).hexdigest()

def main():
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    for html_path in html_files:
        template_name = os.path.basename(html_path)
        token = generate_token(template_name)
        # Store in test db only
        obj, created = TemplateTokenLog.objects.get_or_create(template_name=template_name)
        obj.token = token
        obj.save()
        print(f"Saved token for {template_name} in test DB: {token}")

        # Clean up old tokens and insert only the new one
        with open(html_path, 'r+') as f:
            content = f.read()
            # Remove all existing token comments
            cleaned = re.sub(r'<!-- TOKEN: [a-f0-9]{64} -->\s*', '', content)
            # Insert the new token at the top
            f.seek(0)
            f.write(f"<!-- TOKEN: {token} -->\n" + cleaned)
            f.truncate()

def generate_template_tokens():
    """
    Alias to trigger template tokenisation for all HTML files (test DB only).
    """
    main()

if __name__ == "__main__":
    generate_template_tokens()
