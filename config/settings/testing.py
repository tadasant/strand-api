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


# Algolia
# https://github.com/algolia/algoliasearch-django#install
ALGOLIA = {
    'APPLICATION_ID': 'TEST_ID',
    'API_KEY': 'TEST_KEY',
    'AUTO_INDEXING': True,
    'INDEX_PREFIX': 'test',
}

# Sendgrid
# https://github.com/elbuo8/sendgrid-django
SENDGRID_API_KEY = 'SENDGRID_API_KEY'
NEW_ACCOUNT_TEMPLATE_ID = '100100ABC'
