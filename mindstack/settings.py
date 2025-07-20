from dotenv import load_dotenv # type: ignore
load_dotenv()

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# secret key
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# CSRF trusted origins for production and staging
CSRF_TRUSTED_ORIGINS = [
    "https://mindstack.syafiqkay.com",
    "https://syafiq-kay-2.onrender.com",
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'progress',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mindstack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mindstack.wsgi.application'


# Database
import dj_database_url # type: ignore
if database_url := os.environ.get("DATABASE_URL"):
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=600)
    }
elif all(var in os.environ for var in [
    'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST'
]):
    DB_ENGINE = os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.postgresql')
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.environ.get('DB_NAME', 'mydatabase'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'mysecretpassword'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# --- static files configuration for Azure Blob Storage ---
AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER", "static")
STATIC_LOCATION = AZURE_CONTAINER
STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
AZURE_SSL = True
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'