from configurations import values

from core.settings.base import BaseConfiguration


class Prod(BaseConfiguration):

    DEBUG = False
    SECRET_KEY = values.Value(environ_name='SECRET_KEY')
    ALLOWED_HOSTS = values.ListValue(environ_name='ALLOWED_HOSTS')
