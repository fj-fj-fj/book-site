import logging.config

from core.settings.base import BaseConfiguration, values


class Dev(BaseConfiguration):

    SECRET_KEY = values.SecretValue(environ_name='SECRET_KEY')

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = ['*']

    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')

    @property
    def INSTALLED_APPS(self) -> list[str]:  # type: ignore
        return super().INSTALLED_APPS + [
            'debug_toolbar',
        ]

    @property
    def MIDDLEWARE(self) -> list[str]:  # type: ignore
        return super().MIDDLEWARE + [
            'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
        ]

    LOCAL_LOGGING = {
        'version': 1,
        'formatters': {
            'rich': {
                'datefmt': '[%X]',
                'rich_traceback': True,
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'rich.logging.RichHandler',
                'formatter': 'console',
            },
        },
    }

    BaseConfiguration.BASE_LOGGING['handlers'] |= LOCAL_LOGGING['handlers']  # type: ignore
    logging.config.dictConfig(BaseConfiguration.BASE_LOGGING)
