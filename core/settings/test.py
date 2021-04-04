from core.settings.dev import Dev


class Test(Dev):

    SECRET_KEY = 'test_secret_key'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': Dev.ROOT_DIR / 'db.sqlite3',
        },
    }
