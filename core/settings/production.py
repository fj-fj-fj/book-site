from configurations import values

from core.settings.base import BaseConfiguration


class Prod(BaseConfiguration):

    DEBUG = False
    SECRET_KEY = values.Value(environ_name='SECRET_KEY')
    ALLOWED_HOSTS = values.ListValue(environ_name='ALLOWED_HOSTS')

    # email
    EMAIL_SUBJECT_PREFIX = values.Value('[default prefix :)]')
    DEFAULT_FROM_EMAIL = values.Value(environ_name='EMAIL_HOST_USER')
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = values.Value(environ_name='EMAIL_HOST')
    EMAIL_HOST_USER = values.Value(environ_name='EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = values.Value(environ_name='EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
