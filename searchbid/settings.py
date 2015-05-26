"""
Django settings for searchbid project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ss!x!8tgpkzovj$cde8%!6it(zg)n&rv@z6r+12rnkr_#qq=7k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR , '../templates').replace('\\','/'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# Application definition

INSTALLED_APPS = (
    'material',
    'material.admin',
    'material.frontend',
    'easy_pjax',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'search',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'material.frontend.middleware.SmoothNavigationMiddleware',
)

ROOT_URLCONF = 'searchbid.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                "django.core.context_processors.i18n",
                'django.contrib.messages.context_processors.messages',
                'material.frontend.context_processors.modules',
            ],
        },
    },
]

WSGI_APPLICATION = 'searchbid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
#}

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

MEDIA_URL = '/media/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ["*"]
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'

