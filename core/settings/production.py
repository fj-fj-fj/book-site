import os

from core.settings.base import BaseConfiguration


class Prod(BaseConfiguration):
    DEBUG = False
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
