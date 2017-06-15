How it works
============

The simplest way to get a param value is:

.. code-block:: python

    from apconf import Options

    opts = Options()
    APP_SLUG = opts.get('APP_SLUG', 'apsl-app')

We get the APP_SLUG, with the default value 'apsl-app'. Besides, *kaio* stores
internally the request default value, in order to inform the management scripts.
(See below).


settings.py
-----------

We configure the settings through classes, using *django-configurations*.
We can use the mixins, so that the repetitive configurations rest into the mixin,
centralizing the parametrization and saving code.

**Important** Make sure that *Settings* is the last class in the class definition:

Basic app settings sample:

.. code-block:: python

    import os
    from os.path import join

    from configurations import Configuration
    from django.contrib.messages import constants as messages
    from kaio import Options
    from kaio.mixins import (CachesMixin, DatabasesMixin, CompressMixin, LogsMixin,
                             PathsMixin, SecurityMixin, DebugMixin, WhiteNoiseMixin)


    opts = Options()


    class Base(CachesMixin, DatabasesMixin, CompressMixin, PathsMixin, LogsMixin,
               SecurityMixin, DebugMixin, WhiteNoiseMixin, Configuration):
        """
        Project settings for development and production.
        """

        DEBUG = opts.get('DEBUG', True)

        THUMBNAIL_FORCE_OVERWRITE = True

        BASE_DIR = opts.get('APP_ROOT', None)
        APP_SLUG = opts.get('APP_SLUG', 'test-project')
        SITE_ID = 1
        SECRET_KEY = opts.get('SECRET_KEY', 'key')

        USE_I18N = True
        USE_L10N = True
        USE_TZ = True
        LANGUAGE_CODE = 'es'
        TIME_ZONE = 'Europe/Madrid'

        ROOT_URLCONF = 'main.urls'
        WSGI_APPLICATION = 'main.wsgi.application'

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'kaio',
            '...',
        ]

        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

Using mixins, almost we have only to configure the INSTALLED_APPS.
For further configurations we'll adding more mixins.


