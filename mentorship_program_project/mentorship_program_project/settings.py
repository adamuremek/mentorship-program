"""
Django settings for mentorship_program_project project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import saml2
import saml2.saml
from os import path

# Load .env file
load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.environ.get('DEBUG'):
    DEBUG = os.environ.get('DEBUG').lower() == 'true' or os.environ.get('DEBUG').lower() == '1'


if(DEBUG):
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', default='').split(' ')


# We need to add any origins that the server is hosted on to this list.
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', default='').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'mentorship_program_app',

    'djangosaml2',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'djangosaml2.middleware.SamlSessionMiddleware',
]


if DEBUG:
    # debug tool to help with query stuff
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
    INSTALLED_APPS.append(
            'debug_toolbar'
            ) 
    MIDDLEWARE.append(
                "debug_toolbar.middleware.DebugToolbarMiddleware",
            )
INTERNAL_IPS = [
    "127.0.0.1"
]

ROOT_URLCONF = 'mentorship_program_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mentorship_program_app.view_routes.navigation.global_nav_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'mentorship_program_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if(os.environ.get('DB_ENGINE')):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DB_ENGINE'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# set up user loaded media urls

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Gmail SMTP port for STARTTLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'wingsmentorapp@gmail.com'
EMAIL_HOST_PASSWORD = 'rjrl aldq kjee ybfv'


# For saml auth
SESSION_COOKIE_SECURE = True
SAML_SESSION_COOKIE_SAMESITE = 'None'

AUTHENTICATION_BACKENDS = [
    'djangosaml2.backends.Saml2Backend',
    'django.contrib.auth.backends.ModelBackend',
]

# Redirect here to log in with saml
LOGIN_URL = '/saml2/login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Redirects for after sucessful saml login and logout
LOGIN_REDIRECT_URL = '/saml/login'
ACS_DEFAULT_REDIERCT_URL = '/saml/login'
LOGOUT_REDIRECT_URL = '/logout'

# Create a new django user if they don't exist
SAML_CREATE_UNKNOWN_USER = True

# Attribute to check against existing django users
SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'email'
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = '__iexact'

SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_REDIRECT
SAML_IGNORE_LOGOUT_ERRORS = True

SAML_ATTRIBUTE_MAPPING = {
    'emailAddress': ('email', ),
    'givenName': ('firstName', ),
    'surname': ('lastName', ),
    'objectidentifier': ('id', ),
}

# From djangosaml2 docs
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': f'https://{os.environ.get('DOMAIN')}/saml2/metadata/',

  # directory with attribute mapping
  #'attribute_map_dir': path.join(BASE_DIR, 'saml/attribute-maps'),

  # Permits to have attributes not configured in attribute-mappings
  # otherwise...without OID will be rejected
  'allow_unknown_attributes': True,

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'WINGS Development',
          'name_id_format': saml2.saml.NAMEID_FORMAT_TRANSIENT,

          # For Okta add signed logout requests. Enable this:
          # "logout_requests_signed": True,

          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  (f'https://{os.environ.get('DOMAIN')}/saml2/acs/',
                   saml2.BINDING_HTTP_POST),
                  ], 
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  # Disable next two lines for HTTP_REDIRECT for IDP's that only support HTTP_POST. Ex. Okta:
                  (f'https://{os.environ.get('DOMAIN')}/saml2/ls/',
                   saml2.BINDING_HTTP_REDIRECT),
                  (f'https://{os.environ.get('DOMAIN')}/saml2/ls/post',
                   saml2.BINDING_HTTP_POST),
                  ],
              },

          'signing_algorithm':  saml2.xmldsig.SIG_RSA_SHA256,
          'digest_algorithm':  saml2.xmldsig.DIGEST_SHA256,

           # Mandates that the identity provider MUST authenticate the
           # presenter directly rather than rely on a previous security context.
          'force_authn': False,

           # Enable AllowCreate in NameIDPolicy.
          'name_id_format_allow_create': False,

           # attributes that this project need to identify a user
          'required_attributes': [
                                  'ObjectIdentifier',
                                  'Email',
                                  'Given Name',
                                  'Surname',
                                  ],

           # attributes that may be useful to have but not required
          #'optional_attributes': ['eduPersonAffiliation'],

          'want_response_signed': False,
          'authn_requests_signed': True,
          'logout_requests_signed': True,
          # Indicates that Authentication Responses to this SP must
          # be signed. If set to True, the SP will not consume
          # any SAML Responses that are not signed.
          'want_assertions_signed': True,

          'only_use_keys_in_metadata': True,

          # When set to true, the SP will consume unsolicited SAML
          # Responses, i.e. SAML Responses for which it has not sent
          # a respective SAML Authentication Request.
          'allow_unsolicited': True,

          # in this section the list of IdPs we talk to are defined
          # This is not mandatory! All the IdP available in the metadata will be considered instead.
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              os.environ.get('SAML_IDP_ENTITY_ID'): {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: os.environ.get('SAML_IDP_SSO_URL'),
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_POST: os.environ.get('SAML_IDP_SLO_URL'),
                      }
                  },
              },
          },
      },

  # where the remote metadata is stored, local, remote or mdq server.
  # One metadatastore or many ...
  'metadata': {
      #'local': [path.join(BASE_DIR, 'saml/remote_metadata.xml')],
      'remote': [{"url": os.environ.get('SAML_IDP_METADATA_URL')}],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # Signing
  'key_file': path.join(BASE_DIR, 'saml/private.key'),  # private part
  'cert_file': path.join(BASE_DIR, 'saml/public.pem'),  # public part

  # Encryption
  'encryption_keypairs': [{
      'key_file': path.join(BASE_DIR, 'saml/private.key'),  # private part
      'cert_file': path.join(BASE_DIR, 'saml/public.pem'),  # public part
  }],
}