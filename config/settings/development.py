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

# Slack credentials
SLACK_CLIENT_SECRET = '6d78f8dc3bb99ce00bb172ef662a8389'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'

# Discussion settings
MIN_UNTIL_STALE = 30.0
AUTO_CLOSE_DELAY = 60

SLACK_APP_VERIFICATION_TOKEN = 'anoTH3rRANDoMCOmbo'
SLACK_APP_STALE_DISCUSSION_ENDPOINT = 'http://slackapp.com/stalediscussions'
SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT = 'http://slackapp.com/autocloseddiscussions'
SLACK_APP_SLACK_AGENT_ENDPOINT = 'http://slackapp.com/slackagents'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# CORS
# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_PREFLIGHT_MAX_AGE = 0
