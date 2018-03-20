import os

# Prevent HTTP Host header attacks
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['strand-api-development.us-east-1.elasticbeanstalk.com', 'development.api.trystrand.com']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT']
    }
}

ENABLE_GRAPHIQL = True

# SSL/HTTPS
# https://docs.djangoproject.com/en/2.0/topics/security/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

# django-storages
# http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

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
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
NEW_ACCOUNT_TEMPLATE_ID = os.environ['NEW_ACCOUNT_TEMPLATE_ID']
