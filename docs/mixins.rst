Mixins
======

The mixins are defined in kaio/mixins and inherit from **Object**. They are defined from a function that takes
the name from the .ini (onwards app.ini) file section.

The params into the app.ini file are set without quotation marks, either are numbers, texts, strings, etc.

CachesMixin
-----------

This mixin allows us to configure the cache of our application. It is intended for use with ``Redis`` in
production. If a cache type is not defined, it means that we have ``dummy`` cache.

.. code-block:: python

    from kaio.mixins import CachesMixin

**Section**: Cache

**Parameters**

**CACHE_TYPE**
    cache tupe, by default ``locmem``, options: ``locmem``, ``redis``, ``dummy``

**CACHE_REDIS_DB**
    redis database number that we'll use as cache into redis. By default, ``2``.

**CACHE_REDIS_PASSWORD**
    redis for password. By default without password.

**REDIS_HOST**
    redis host name. By default ``localhost``

**REDIS_PORT**
    port of the redis server. By default ``6379``

**CACHE_PREFIX**
    prefix to use in the cache keys for the projecte. By default is the project ``SLUG``.

**CACHE_TIMEOUT**
    Cache expiration time. By default ``3600`` secons, 1 hour.

**CACHE_MAX_ENTRIES**
    Maximum number of cached entries. By default ``10000``.


CeleryMixin
-----------

This mixin allows us to configure Celery_ in case we use it in our application.

.. _Celery: http://docs.celeryproject.org/en/latest/index.html

.. code-block:: python

    from kaio.mixins import CeleryMixin

**Section**: Cache

**Parameters**

**CELERY_RESULT_BACKEND**
    todo

**CELERY_ALWAYS_EAGER**
    Default ``True``.

**CELERY_EAGER_PROPAGATES_EXCEPTIONS**
    Default ``True``.

**CELERY_IGNORE_RESULT**
    Default ``True``.

**CELERY_MAX_CACHED_RESULTS**
    Default ``5000``.

**BROKER_TYPE**
    Default ``redis``.

**CELERY_REDIS_BROKER_DB**
    Default ``0``.

**CELERY_REDIS_RESULT_DB**
    Default ``0``.

**RABBITMQ_HOST**
    Default ``localhost``.

**RABBITMQ_PORT**
    Default ``5672``.

**RABBITMQ_USER**
    Default ``guest``.

**RABBITMQ_PASSWD**
    Default ``guest``.

**RABBITMQ_VHOST**
    Default ``/``.

**BROKER_URL**
    todo


CmsMixin
--------

.. warning:: Deprecated mixin

Mixin that helps us to get the languages configured on the project.

.. code-block:: python

    from kaio.mixins import CMSMixin

**Section**: Compress

**Parameters**


CompressMixin
-------------

django-compressor_ configuration.

.. _django-compressor: http://django-compressor.readthedocs.org/en/latest/settings/

.. code-block:: python

    from kaio.mixins import CompressMixin

**Section**: Compress

**Parameters**

**COMPRESS_DEBUG_TOGGLE**
    by default ``nocompress`` in DEBUG mode.

**COMPRESS_ENABLED**
    by default ``False``.

**COMPRESS_CSS_HASHING_METHOD**
    by default ``content``.

**COMPRESS_LESSC_ENABLED**
    by default ``True``.

**COMPRESS_SASS_ENABLED**
    by default ``True``.

**COMPRESS_BABEL_ENABLED**
    by default ``False``.

**COMPRESS_LESSC_PATH**
    by default ``lessc``.

**COMPRESS_SASS_PATH**
    by default ``node-sass``.

**COMPRESS_BABEL_PATH**
    by default ``babel``.

**COMPRESS_PRECOMPILERS**
    by default includes automatically less, babel and coffeescript if they are active.

**COMPRESS_OUTPUT_DIR**
    by default ``CACHE/``.

**COMPRESS_OFFLINE**
    by default ``False``.

**COMPRESS_OFFLINE_TIMEOUT**
    by default ``31536000`` (1 year in seconds).

**COMPRESS_OFFLINE_MANIFEST**
    by default ``manifest.json``.


**Static offline compression**

In order to be able to use it you have to follow two steps:

* add COMPRESS_OFFLINE = True to app.ini file
* the ``{% compress js/css %}`` can not have any django logic, no vars, no templatetags, no subblocks...

This last step is advisable to follow it as a good practice just in case
in any future moment we want the **COMPRESS_OFFLINE** feature.

Example of the [Compress] section with compress activated, with coffescript support and
compress offline activated. **LESS** suport is active by default:

.. code-block:: python

    ...
    [Compress]
    COMPRESS_ENABLED = True
    COMPRESS_COFFEE_ENABLED = True
    COMPRESS_OFFLINE = True
    ...

The idea is to have COMPRESS_OFFLINE = False in development environment and to
have COMPRESS_OFFLINE = True once we deploy the project to production environment.


In order to test it in development environment you have to execute

.. code-block:: python

    python manage.py collectstatic

and then

.. code-block:: python

    python manage.py compress


DatabaseMixin
-------------

Database access configuration.

.. code-block:: python

    from kaio.mixins import DatabasesMixin

**Section**: Database

**Parameters**

**DATABASE_ENGINE**
    by default ``sqlite3``, allow ``sqlite3``, ``postgresql_psycopg2``, ``mysql``, ``oracle``

**DATABASE_NAME**
    default name, if we use ``sqlite3`` it will be ``db.sqlite``

**DATABASE_USER**
    user to use

**DATABASE_PASSWORD**
    password

**DATABASE_HOST**
    host name

**DATABASE_PORT**
    port number

**DATABASE_CONN_MAX_AGE**
    by default ``0``.

**DATABASE_OPTIONS_OPTIONS**
    string to add to database options setting. Empty by default. Example to change the postgresql schema: ``DATABASE_OPTIONS_OPTIONS = -c search_path=some_schema``


DebugMixin
----------
This mixin allows us to define and work with the debug parameters and configure ``django-debug-toolbar``
to be used in our application. Therefore its use depends on whether this module is configured
in the ``requirements.txt`` of the project, otherwise we will not have activated the option of the ``debug toolbar``.

.. code-block:: python

    from kaio.mixins import DebugMixin

**Section**: Debug

**Parameters**

**DEBUG**
    by default ``False``.

**TEMPLATE_DEBUG**
    by default same as **DEBUG**.

**ENABLE_DEBUG_TOOLBAR**
    by default same as **DEBUG**. ``False`` if the module is not installed.

**ALLOWED_HOSTS**
    allowed hosts. No value by default. It must be set always in production.

EmailMixin
----------

Set the basic parameters by default to configure the mail. In its configuration by default allows us to
operate with ``django-yubin``, leaving its final configuration for the production environment.

.. code-block:: python

    from kaio.mixins import EmailMixin

**Section**: Email

**Parameters**

**DEFAULT_FROM_EMAIL**
    by default ``Example <info@example.com>``.

**EMAIL_BACKEND**
    by default ``django.core.mail.backends.smtp.EmailBackend`` or ``django_yubin.smtp_queue.EmailBackend`` if django_yubin is installed.

**EMAIL_FILE_PATH**
    by default ``None``.

**EMAIL_HOST**
    by default ``localhost``.

**EMAIL_HOST_PASSWORD**
    by default ``''``.

**EMAIL_HOST_USER**
    by default ``''``.

**EMAIL_PORT**
    by default ``25``.

**EMAIL_SUBJECT_PREFIX**
    Prefix to add to Django's subject. By default `[Django]`

**EMAIL_USE_TLS**
    by default ``False``.

**MAILER_PAUSE_SEND**
    by default ``False``.

**MAILER_USE_BACKEND**
    by default ``django.core.mail.backends.smtp.EmailBackend``.

**MAILER_MAIL_ADMINS_PRIORITY**
    by default ``None``.

**MAILER_MAIL_MANAGERS_PRIORITY**
    by default ``None``.

**MAILER_EMPTY_QUEUE_SLEEP**
    by default ``30``.

**MAILER_LOCK_WAIT_TIMEOUT**
    by default ``0``.

**MAILER_LOCK_PATH**
    by default ``os.path.join(self.APP_ROOT, "send_mail")``.

Recall that in order to use django_yubin_ we must configure the **cron**.

.. _django_yubin: http://django-yubin.readthedocs.org/en/latest/settings.html


FilerMixin
----------

.. todo:: FilerMixin - Complete description

.. code-block:: python

    from kaio.mixins import FilerMixin

**Section**: Filer

**Parameters**

**FILER_IS_PUBLIC_DEFAULT**
    Default ``True``.

**FILER_ENABLE_PERMISSIONS**
    Default ``False``.

**FILER_DEBUG**
    Default ``False``.

**FILER_ENABLE_LOGGING**
    Default ``False``.

**FILER_0_8_COMPATIBILITY_MODE**
    Default ``False``.

**THUBMNAIL_DEBUG**
    Default ``False``.

**THUMBNAIL_QUALITY**
    Default ``85``.

**FILER_CUSTOM_NGINX_SERVER**
    Default ``False``.

**DEFAULT_FILE_STORAGE**
    Default ``django.core.files.storage.FileSystemStorage``.

**FILER_CUSTOM_SECURE_MEDIA_ROOT**
    Default ``filer_private``.


LogsMixin
---------

Mixin that handles the configuration the Django logs. Established some default configurations that we use
in our development and production environments for the project configuration.

.. code-block:: python

    from kaio.mixins import LogsMixin

**Section**: Logs

**Parameters**

**EMAIL_SUBJECT_PREFIX**
    Prefix to add to Django's subject. By default `[Django]`

**Section**: Logs

**Parameters**

**LOG_LEVEL**
    sets the project logging level. By default: ``DEBUG``

**DJANGO_LOG_LEVEL**
    sets the django logging level. By default: ``ERROR``

**LOG_FILE**
    name of the log file. No established by default, usually specified in production.

**EXTRA_LOGGING**
    parameter that sets the log level at module level in a easy way. It does not have a default value.
    As a parameter we have to set a module list with the differents levels to log each separated by comma
    in the followinf format: ``<module>:log_value``
    E.g.:

.. code-block:: python

    [Logs]
    EXTRA_LOGGING = oscar.paypal:DEBUG, django.db:INFO

**SENTRY_ENABLED**
    by default ``False``.

**SENTRY_DSN**
    by default ``''``.

**SENTRY_TRANSPORT**
    by default ``'raven.transport.threaded.ThreadedHTTPTransport'``.


PathsMixin
----------

Paths base settings.

.. code-block:: python

    from kaio.mixins import PathsMixin

**Section**: Paths

**Parameters**

**APP_ROOT**
    By default the current directory, ``abspath('.')``.

**MEDIA_ROOT**
    By default the current ``APP_ROOT`` + ``/media``.

**STATIC_URL**
    By default ``/static/``.

**MEDIA_URL**
    By default ``/media/``.

**STATIC_ROOT**
    By default ``abspath(join("/tmp", "{}-static".format(self.APP_SLUG))``.



SecurityMixin
-------------

Security base settings.

.. code-block:: python

    from kaio.mixins import SecurityMixin

**Section**: Security

**Parameters**

**SECRET_KEY**
    A secret key for a particular Django installation.
    This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
    By default ``''``.

**ALLOWED_HOSTS**
    A list of strings representing the host/domain names that this Django site can serve.
    By default ``[]``.

**SECURE_PROXY_SSL_HEADER_NAME**
    user to use
    The name of the header to configure the proxy ssl. By default ``HTTP_X_FORWARDED_PROTO``

**SECURE_PROXY_SSL_HEADER_VALUE**
    The value of the header to configure the proxy ssl. By default ``https``

**SECURE_PROXY_SSL_HEADER**
    A tuple representing a HTTP header/value combination that signifies a request is secure.
    This controls the behavior of the request object’s is_secure() method.
    By default returns the tuple of the combination of the ``SECURE_PROXY_SSL_HEADER_NAME`` and ``SECURE_PROXY_SSL_HEADER_VALUE``.
    https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header


WhiteNoiseMixin
---------------

Automatic configuration for static serving using whitenoise_. You must have version 3 installed.

.. _whitenoise: http://whitenoise.evans.io/

.. code-block:: python

    from kaio.mixins import WhiteNoiseMixin

**Parameters**

**ENABLE_WHITENOISE**
    by default ``False``. ``False`` if the module is not installed.

**WHITENOISE_AUTOREFRESH**
    by default ``True``.

**WHITENOISE_USE_FINDERS**
    by default ``True``.
