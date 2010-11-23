try:
    from djangoappengine.settings_base import *
    has_djangoappengine = True
except ImportError:
    has_djangoappengine = False
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

import os

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'djangotoolbox',
    'mediagenerator',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_openid_auth',
    'techism2.events',
    'techism2.orgs',
    'techism2'
)

if has_djangoappengine:
    INSTALLED_APPS = ('djangoappengine',) + INSTALLED_APPS

TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

LANGUAGE_CODE = 'de-DE'
USE_I18N = True
USE_L10N = True

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devmedia/'
PRODUCTION_MEDIA_URL = '/media/'
GLOBAL_MEDIA_DIRS = (os.path.join(os.path.dirname(__file__), 'media'),)

MEDIA_BUNDLES = (
    ('base.css',
        'css/style.css',
        'css/jquery/jquery-ui-1.8.5.custom.css',
    ),
    ('base.js',
        'js/jquery/jquery-1.4.2.min.js',
        'js/jquery/jquery-ui-1.8.6.custom.min.js',
        'js/jquery/jquery.infinitescroll.min.js',
        'js/modernizr-1.6.min.js',
        'js/googlemaps.js',
    ),
    ('events-index.js',
        'js/events/index.js',
    ),
    ('events-details.js',
        'js/events/details.js',
    ),
    ('events-create.js',
        'js/jquery/jquery.ui.datepicker-de.js',
        'js/events/create.js',
    ),
)

ROOT_URLCONF = 'urls'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
else:
    EMAIL_BACKEND = 'djangoappengine.mail.EmailBackend'

OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

if not DEBUG:
    SESSION_COOKIE_SECURE = True

MIDDLEWARE_CLASSES = (
    # Media middleware has to come first
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'techism2.middleware.SecureRequiredMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'gaeauth.backends.GoogleAccountBackend',
    'django_openid_auth.auth.OpenIDBackend'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.contrib.staticfiles.context_processors.staticfiles',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)


GAE_SETTINGS_MODULES = (
    'gae_settings',
)

from techism2 import service
SECRET_KEY = service.get_secret_key()
