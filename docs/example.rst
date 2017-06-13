Application example
===================


Example from scratch. The kiosk
-------------------------------

1. We execute

.. code-block:: python

    django-admin.py startporject kiosk

Since we do not want the project and the application to be called the same we will
rename the main directory of `kiosk` to` prj_kiosk` and we move all within the ``src``
directory of the project. We will change the name of the srcf folder to ``main``
so that` kiosko` will be free if we want to create there the data model.


2. We create the requirements file in the project directory and create
the requirements to proceed to create the virtual environment.

.. code-block:: python

    # requirements.txt
    Django==1.10.7
    django-appconf==1.0.2
    django_compressor==2.1
    django-extensions==1.7.2
    django-kaio==0.7.1
    django-logentry-admin==1.0.2
    django-redis==4.4.4
    django-robots==2.0
    django-storages==1.5.2
    django-yubin==0.3.1
    psycopg2==2.6.2
    pytz==2016.6.1
    redis==2.10.5
    requests==2.17.3

with the versions we need

3. Modify ``manage.py`` and ``wsgi.py`` as explained in the :ref:`config wsgi.py and manage.py` section.

4. Replace the settings.py by our custom version of it. E.g.:

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
        APP_SLUG = opts.get('APP_SLUG', 'kiosk')
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
            # django
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            # apps
            'kiosk',
            'main',

            # 3rd parties
            'compressor',
            'constance',
            'cookielaw',
            'constance.backends.database',
            'django_extensions',
            'django_yubin',
            'kaio',
            'logentry_admin',
            'robots',
            'sorl.thumbnail',
            'bootstrap3',
            'storages',
            'django_tables2',
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

        # SecurityMiddleware options
        SECURE_BROWSER_XSS_FILTER = True

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    os.path.join(BASE_DIR, 'sfc_test_portal/templates/'),
                ],
                'OPTIONS': {
                    'context_processors': [
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.static",
                        "django.contrib.messages.context_processors.messages",
                        "django.template.context_processors.tz",
                        'django.template.context_processors.request',
                        'constance.context_processors.config',
                    ],
                    'loaders': [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]
                },
            },
        ]
        if not DEBUG:
            TEMPLATES[0]['OPTIONS']['loaders'] = [
                ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
            ]

        # Email
        EMAIL_BACKEND = 'django_yubin.smtp_queue.EmailBackend'
        DEFAULT_FROM_EMAIL = opts.get('DEFAULT_FROM_EMAIL', 'Example <info@example.com>')
        MAILER_LOCK_PATH = join(BASE_DIR, 'send_mail')

        # Bootstrap 3 alerts integration with Django messages
        MESSAGE_TAGS = {
            messages.ERROR: 'danger',
        }

        # Constance
        CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
        CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
        CONSTANCE_CONFIG = {
            'GOOGLE_ANALYTICS_TRACKING_CODE': ('UA-XXXXX-Y', 'Google Analytics tracking code.'),
        }


5. Generate the .ini file in the ``src`` directory executing:

.. code-block:: python

    python manage.py generate_ini > app.ini

and then modify the default parameters we have. In particular we will have to modify
the database connection and put the application in debug mode.

6. Execute the migrations:

.. code-block:: python

    python manage.py syndb --all

And we proceed as always.

7. We need to modify ``main/urls.py`` to be able to serve the static content while we are in debug mode.

.. code-block:: python

    from django.conf.urls import patterns, include, url
    from django.conf import settings

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        # Examples:
        url(r'^$', 'kiosk.views.home', name='home'),
        url(r'^kiosk/', include('kiosk.foo.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )

    if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


And finally we run

.. code-block:: python

    python manage.py apsettings

to check the **settings** of our application.

If we need to add an application settings we have two options:

1. Generate a mixin for the particular module, if it has to be reusable.
2. Add such configuration in our settings.py base class.

