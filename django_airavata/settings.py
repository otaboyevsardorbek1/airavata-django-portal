"""
Django settings for django_airavata_gateway project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from importlib import import_module

from pkg_resources import iter_entry_points

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bots0)m91u_i4gpw+103o%2jn#j57wjh7s@9$x*27_4^*jyku4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_airavata.apps.admin.apps.AdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_airavata.apps.auth.apps.AuthConfig',
    'django_airavata.apps.workspace.apps.WorkspaceConfig',
    'rest_framework',
    'django_airavata.apps.api.apps.ApiConfig',
    'django_airavata.apps.groups.apps.GroupsConfig',
    'django_airavata.apps.dataparsers.apps.DataParsersConfig',
    'django.contrib.humanize',

    # wagtail related apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.styleguide',

    # wagtail third party dependencies
    'modelcluster',
    'taggit',
    'wagtailfontawesome',
    'wagtail_draftail_anchors',

    # wagtail custom apps
    'django_airavata.wagtailapps.base.apps.BaseConfig',

    # django-webpack-loader
    'webpack_loader',

    # Airavata Django Portal SDK
    'airavata_django_portal_sdk',
]

# List of app labels for Airavata apps that should be hidden from menus
# For example: HIDDEN_AIRAVATA_APPS = ['django_airavata_dataparsers']
HIDDEN_AIRAVATA_APPS = []

# AppConfig instances from custom Django apps
CUSTOM_DJANGO_APPS = []

# Add any custom apps installed in the virtual environment
# Essentially this looks for the entry_points metadata in all installed Python packages. The format of the metadata in setup.py is the following:
#
#    setuptools.setup(
#        ...
#        entry_points="""
#    [airavata.djangoapp]
#    dynamic_djangoapp = dynamic_djangoapp.apps:DynamicDjangoAppConfig
#    """,
#        ...
#    )
#
for entry_point in iter_entry_points(group='airavata.djangoapp'):
    custom_app_class = entry_point.load()
    custom_app_instance = custom_app_class(
        entry_point.name, import_module(entry_point.module_name))
    CUSTOM_DJANGO_APPS.append(custom_app_instance)
    # Create path to AppConfig class (otherwise the ready() method doesn't get
    # called)
    INSTALLED_APPS.append("{}.{}".format(entry_point.module_name,
                                         entry_point.attrs[0]))

OUTPUT_VIEW_PROVIDERS = {}
for entry_point in iter_entry_points(group='airavata.output_view_providers'):
    OUTPUT_VIEW_PROVIDERS[entry_point.name] = entry_point.load()()

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_airavata.apps.auth.middleware.authz_token_middleware',
    'django_airavata.middleware.AiravataClientMiddleware',
    'django_airavata.middleware.profile_service_client',
    # Needs to come after authz_token_middleware, airavata_client and
    # profile_service_client
    'django_airavata.apps.auth.middleware.gateway_groups_middleware',
    # Wagtail related middleware
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'django_airavata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "django_airavata", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_airavata.context_processors.airavata_app_registry',
                'django_airavata.context_processors.custom_app_registry',
                'django_airavata.context_processors.get_notifications',
                'django_airavata.context_processors.user_session_data',
                'django_airavata.context_processors.google_analytics_tracking_id',
                # 'django_airavata.context_processors.resolver_match',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_airavata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "django_airavata", "static")]

# Media Files (PDF, Documents, Custom Images)
MEDIA_ROOT = os.path.join(BASE_DIR, "django_airavata", "media")
MEDIA_URL = '/media/'

# Data storage
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_FILE_SIZE = 64 * 1024 * 1024  # 64 MB
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django_airavata.uploadhandler.MaxFileSizeTemporaryFileUploadHandler',
]

# Tus upload
# Override and set to a valid tus endpoint, for example
# "http://localhost:1080/files/"
TUS_ENDPOINT = None
# Override and set to the directory where tus uploads will be stored
TUS_DATA_DIR = None

# Legacy (PGA) Portal link - provide a link to the legacy portal
PGA_URL = None

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'django_airavata.apps.api.authentication.OAuthAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER':
        'django_airavata.apps.api.exceptions.custom_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

AUTHENTICATION_BACKENDS = [
    'django_airavata.apps.auth.backends.KeycloakBackend'
]

# Default email backend (for local development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Wagtail related stuff
WAGTAIL_SITE_NAME = 'Django Airavata Portal'

WAGTAILIMAGES_JPEG_QUALITY = 100

# For some long wagtail pages, the number of POST parameters exceeds 1000,
# which is the default for DATA_UPLOAD_MAX_NUMBER_FIELDS
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

LOGIN_URL = 'django_airavata_auth:login'
LOGIN_REDIRECT_URL = 'django_airavata_workspace:dashboard'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_OPTIONS = {
    # Control whether username/password authentication is allowed
    'password': {
        'name': 'your account',
        # Static path to image
        # 'logo': '/static/path/to/image'
    },
    # Can have multiple external logins
    # 'external': [
    #     {
    #         'idp_alias': 'cilogon',
    #         'name': 'CILogon',
    #         # Static path to image
    #         'logo': 'path/to/image'
    #     }
    # ]
}

# Configure the URIs that can be redirected to with /auth/access-token-redirect?redirect_uri=...
# Takes a list of dicts, where the key 'URI' specifies the allowed redirect URI
# and the optional key 'PARAM_NAME' allows specifying the query parameter name
# for the access token parameter (defaults to 'access_token').
ACCESS_TOKEN_REDIRECT_ALLOWED_URIS = []

# Seconds each connection in the pool is able to stay alive. If open connection
# has lived longer than this period, it will be closed.
# (https://github.com/Thriftpy/thrift_connector)
THRIFT_CLIENT_POOL_KEEPALIVE = 5

# Webpack loader
WEBPACK_LOADER = {
    'COMMON': {
        'BUNDLE_DIR_NAME': 'common/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'static',
            'common',
            'dist',
            'webpack-stats.json'),
        'TIMEOUT': 60,
    },
    'ADMIN': {
        'BUNDLE_DIR_NAME': 'django_airavata_admin/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'apps',
            'admin',
            'static',
            'django_airavata_admin',
            'dist',
            'webpack-stats.json'),
        'TIMEOUT': 60,
    },
    'AUTH': {
        'BUNDLE_DIR_NAME': 'django_airavata_auth/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'apps',
            'auth',
            'static',
            'django_airavata_auth',
            'dist',
            'webpack-stats.json'),
    },
    'DATAPARSERS': {
        'BUNDLE_DIR_NAME': 'django_airavata_dataparsers/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'apps',
            'dataparsers',
            'static',
            'django_airavata_dataparsers',
            'dist',
            'webpack-stats.json'),
        'TIMEOUT': 60,
    },
    'GROUPS': {
        'BUNDLE_DIR_NAME': 'django_airavata_groups/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'apps',
            'groups',
            'static',
            'django_airavata_groups',
            'dist',
            'webpack-stats.json'),
        'TIMEOUT': 60,
    },
    'WORKSPACE': {
        'BUNDLE_DIR_NAME': 'django_airavata_workspace/dist/',
        'STATS_FILE': os.path.join(
            BASE_DIR,
            'django_airavata',
            'apps',
            'workspace',
            'static',
            'django_airavata_workspace',
            'dist',
            'webpack-stats.json'),
        'TIMEOUT': 60,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s %(name)s:%(lineno)d %(levelname)s] %(message)s'
        },
    },
    'handlers': {
        # Log everything to the console when DEBUG=True
        'console_debug': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # Only log INFO and higher levels to console when DEBUG=False
        'console': {
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO'
        },
        'mail_admins': {
            'filters': ['require_debug_false'],
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django_airavata': {
            'handlers': ['console', 'console_debug', 'mail_admins'],
            'level': 'DEBUG'
        },
        'root': {
            'handlers': ['console', 'console_debug'],
            'level': 'WARNING'
        }
    },
}


def merge_setting(default, custom_setting):
    # FIXME: only handles dict settings, doesn't handle lists
    if isinstance(custom_setting, dict):
        for k in custom_setting.keys():
            if k not in default:
                default[k] = custom_setting[k]
            else:
                raise Exception("Custom django app setting conflicts with "
                                "key {} in {}".format(k, default))


# Merge settings from custom Django apps
# FIXME: only handles WEBPACK_LOADER additions
for custom_django_app in CUSTOM_DJANGO_APPS:
    if hasattr(custom_django_app, 'settings'):
        s = custom_django_app.settings
        merge_setting(WEBPACK_LOADER, getattr(s, 'WEBPACK_LOADER', {}))

# Allow all settings to be overridden by settings_local.py file
try:
    from django_airavata.settings_local import *  # noqa
except ImportError:
    pass
