# randomly generated secret key by django, can be modified
SECRET_KEY = '*********'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webview',
    }
}

# change stars by password
BROKER_URL = 'redis://:******@localhost:6379/0'
CELERY_RESULT_BACKEND = BROKER_URL
MEDIA_ROOT = '/var/nfs/webview/media'
