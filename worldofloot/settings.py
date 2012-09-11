import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ian', 'ian.webster@gmail.com'),
)

MANAGERS = ADMINS

# Registration settings
ACCOUNT_ACTIVATION_DAYS=14

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'worldofloot',                      # Or path to database file if using sqlite3.
        'USER': 'django_login',                      # Not used with sqlite3.
        'PASSWORD': 'foobar',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
MEDIA_URL = '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ht@%u33725p@u!%p^a2fqsy_s18qaa(pf59g1+t1fbc*233dug'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# message config
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
  message_constants.DEBUG: 'debug',
  message_constants.INFO: 'alert-info',
  message_constants.SUCCESS: 'alert-success',
  message_constants.WARNING: 'alert-warning',
  message_constants.ERROR: 'alert-error',
}


ROOT_URLCONF = 'worldofloot.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Accounts settings
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_PASSWORD_MIN_LENGTH = 1
SOCIALACCOUNT_AUTO_SIGNUP=True
SOCIALACCOUNT_PROVIDERS = \
  {
    'google': {
      'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile']
    },
    'facebook': {
      'SCOPE': [],
      'METHOD': 'oauth2',
      'LOCALE_FUNC': lambda r: 'en_US',
    }
  }

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

BROKER_BACKEND = 'django' # for celery/heroku

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'main',
    'taggit',
    'south',
    'gunicorn',

    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.openid',
)

try:
  from local_settings import *
except ImportError:
  pass

