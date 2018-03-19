import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'strand_api',
        'USER': 'strand',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

ENABLE_GRAPHIQL = False
CSRF_COOKIE_SECURE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# Email
# https://docs.djangoproject.com/en/2.0/topics/email/#module-django.core.mail
# TODO: [API-161] Move from plain-text to SendGrid
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'rAnDoMp@ssW0RD'
EMAIL_PORT = 587

# Algolia
# https://github.com/algolia/algoliasearch-django#install
ALGOLIA = {
    'APPLICATION_ID': 'TEST_ID',
    'API_KEY': 'TEST_KEY',
    'AUTO_INDEXING': True,
    'INDEX_PREFIX': 'test',
}
