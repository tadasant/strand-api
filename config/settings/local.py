import os
import json

# Prevent HTTP Host header attacks
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['docker.for.mac.localhost', 'localhost']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DB_CREDENTIALS = json.load(open(os.path.join(BASE_DIR, 'db.config.json'), 'r'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_CREDENTIALS['NAME'],
        'USER': DB_CREDENTIALS['USER'],
        'PASSWORD': DB_CREDENTIALS['PASSWORD'],
        'HOST': DB_CREDENTIALS['HOST'],
        'PORT': DB_CREDENTIALS['PORT']
    }
}

ENABLE_GRAPHIQL = True
CSRF_COOKIE_SECURE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# CORS
# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_PREFLIGHT_MAX_AGE = 0

# Email
# https://docs.djangoproject.com/en/2.0/topics/email/#module-django.core.mail
EMAIL_SETTINGS = json.load(open(os.path.join(BASE_DIR, 'email.config.json'), 'r'))

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = EMAIL_SETTINGS['EMAIL_USER']
EMAIL_HOST_PASSWORD = EMAIL_SETTINGS['EMAIL_PASSWORD']
EMAIL_PORT = 587
