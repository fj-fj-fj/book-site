from configurations import values

from core.settings.base import BaseConfiguration


class Prod(BaseConfiguration):

    DEBUG = False
    SECRET_KEY = values.Value()
    ALLOWED_HOSTS = values.Value()
