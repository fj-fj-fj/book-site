from pathlib import Path

import dj_database_url
from configurations import Configuration, values
from django.utils.log import DEFAULT_LOGGING


class BaseConfiguration(Configuration):

    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

    DEBUG = values.BooleanValue(True)
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    DATABASES = {
        'default': dj_database_url.config(),
    }

    ROOT_URLCONF = 'core.urls'
    WSGI_APPLICATION = 'core.wsgi.application'

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    THIRD_PARTY_APPS = [
        'social_django',
        'admin_honeypot',
    ]
    LOCAL_APPS = [
        'store',
    ]
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
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

    STATIC_URL = '/static/'

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        ),
    }

    # email
    ADMIN_BASE_URL = values.Value(environ_name='ADMIN_BASE_URL')

    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    EMAIL_TIMEOUT = 5
    ADMINS = [
        ('fj-fj-fj', values.Value(environ_name='ADMIN_BASE_EMAIL')),
    ]
    MANAGERS = ADMINS
    ACCOUNT_EMAIL_VERIFICATION = 'none'

    # social auth
    SOCIAL_AUTH_POSTGRES_JSONFIELD = True

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.github.GithubOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    )

    SOCIAL_AUTH_GITHUB_KEY = values.Value(environ_name='SOCIAL_AUTH_GITHUB_KEY', environ_prefix=None)
    SOCIAL_AUTH_GITHUB_SECRET = values.Value(environ_name='SOCIAL_AUTH_GITHUB_SECRET', environ_prefix=None)

    # logging
    (LOG_DIR := Path(ROOT_DIR.parent / 'log')).is_dir() or LOG_DIR.mkdir(parents=True, exist_ok=True)  # type: ignore
    (WARNING_FILE := LOG_DIR / 'warning.log').is_file() or WARNING_FILE.touch(exist_ok=True)  # type: ignore

    LOGGING_CONFIG = None
    LOGLEVEL = values.Value(environ_name='DJANGO_LOG_LEVEL', default='INFO')
    BASE_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '{module}: {message}',
                'datefmt': '%d/%b/%Y %H:%M:%S',
                'style': '{',
            },
            'file': {
                'format': (
                    '[{asctime}] - {levelname} - ({module}:{lineno}) - '
                    '{process:d} - {thread:d} -- {message}'
                ),
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': WARNING_FILE,
                'formatter': 'file',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'core': {
                'handlers': ['console', 'file'],
                'level': LOGLEVEL,
                'propagate': False,
            },
            'core.accounts': {
                'handlers': ['console', 'file'],
                'level': LOGLEVEL,
                'propagate': False,
            },
        },
    }

    for key in 'formatters', 'handlers', 'loggers':
        BASE_LOGGING[key]['django.server'] = DEFAULT_LOGGING[key]['django.server']  # type: ignore
