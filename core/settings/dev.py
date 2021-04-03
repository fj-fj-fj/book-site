import os

from core.settings.base import BaseConfiguration


class Dev(BaseConfiguration):

    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = [
        'localhost',
        '127.0.0.1',
        '[::1]'
    ]

    @property
    def INSTALLED_APPS(self) -> list[str]:
        return super().INSTALLED_APPS + [
            'debug_toolbar',
        ]

    @property
    def MIDDLEWARE(self) -> list[str]:
        return super().MIDDLEWARE + [
            'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
        ]
