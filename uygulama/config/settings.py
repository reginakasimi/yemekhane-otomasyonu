import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'ders-ortami-gizli-anahtar')
DEBUG = False
ALLOWED_HOSTS = ['*']

# Формы отправляются на адрес Apache. Django должен ему доверять, иначе POST даст ошибку 403.
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080', 'http://127.0.0.1:8080']

INSTALLED_APPS = ['web']

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': ['django.template.context_processors.request']},
}]

# ORM не используем: SQL пишем сами в repositories/
DATABASES = {}

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_TZ = False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}