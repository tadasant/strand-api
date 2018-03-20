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

# Algolia
# https://github.com/algolia/algoliasearch-django#install
ALGOLIA = {
    'APPLICATION_ID': 'E384DX3TAQ',
    'API_KEY': '489c23c36cbf1ee045b4f3c2cfe2f8b5',
    'INDEX_PREFIX': 'dev',
}

# Sendgrid
# https://github.com/elbuo8/sendgrid-django
EMAIL_SETTINGS = json.load(open(os.path.join(BASE_DIR, 'email.config.json'), 'r'))
SENDGRID_API_KEY = EMAIL_SETTINGS['SENDGRID_API_KEY']
NEW_ACCOUNT_TEMPLATE_ID = EMAIL_SETTINGS['NEW_ACCOUNT_TEMPLATE_ID']
