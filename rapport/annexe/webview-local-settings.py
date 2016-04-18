# set to MASTER master's address and password to PASSWORD
MASTER = "*******"
PASSWORD = "*******"

BROKER_URL = 'redis://:%s@%s:6379/0' % (PASSWORD, MASTER)
CELERY_RESULT_BACKEND = BROKER_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webview',
        'USER': 'www-data',
        'PASSWORD': PASSWORD,
        'HOST': MASTER,
    }
}
MEDIA_ROOT = "/mnt/webview/media"
CLAMAV_SOCKET = "/var/run/clamav/clamd.sock"
