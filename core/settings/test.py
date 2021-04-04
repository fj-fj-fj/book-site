import dj_database_url

from core.settings.dev import Dev


class Test(Dev):

    SECRET_KEY = 'test_secret_key'

    DATABASES = {
        'default': dj_database_url.config(default='sqlite://:memory:')
    }
