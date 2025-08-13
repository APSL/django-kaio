==========
Change log
==========

v1.7.0 (2025-08-13)
-------------------

* Support to customize Redis scheme with ``REDIS_SCHEME`` default to ``redis``, this allows to use ``rediss`` (with double S) for TLS connections.
* Support for ``CACHE_REDIS_USER`` to authenticate to redis.
* Update some /docs dependencies with security fixes.
* Update Github Action versions.

v1.6.0 (2025-03-19)
--------------------

* New setting ``ALLOWED_HOSTS_DEBUG_TOOLBAR`` for allowing debug toolbar for some hosts in addition
  to ``INTERNAL_IPS``.
* Update requirements for building docs and use them to create reproducible builds in ReadTheDocs.

v1.5.0 (2023-06-29)
--------------------

* Support Python 3.11 and Django 4.2.
* Migrate ReadTheDocs configuration file to v2.
* GitHub Actions to deploy to PyPI.

v1.4.2 (2023-01-19)
--------------------

* Add more settings for django_yubin: MAILER_STORAGE_DELETE.

v1.4.1 (2023-01-11)
--------------------

* Add more settings for django_yubin: MAILER_HC_QUEUED_LIMIT_OLD, MAILER_STORAGE_BACKEND and
  MAILER_FILE_STORAGE_DIR.

v1.4.0 (2022-09-27)
--------------------

* Add support for django_yubin >= 2.0.0.

v1.3.0 (2022-05-30)
--------------------

* Improve ``CeleryMixin``: better and updated default values and some new settings.

v1.2.0 (2022-05-11)
--------------------

* Add ``AWS_S3_ENDPOINT_URL`` and ``AWS_S3_CUSTOM_DOMAIN`` to ``StorageMixin`` to support CloudFront.

v1.1.0 (2022-05-09)
--------------------

* Add ``SENTRY_IGNORE_LOGGERS`` to allow to avoid sending noisy logs to Sentry.

v1.0.1 (2022-05-05)
--------------------

* Update requirements versions to fix build errors in ReadTheDocs.
* No new features.

v1.0.0 (2022-05-05)
--------------------

* Add new mixin for Sentry SDK and remove old Raven and Sentry settings from LogsMixin.

v0.15.0 (2022-05-02)
--------------------

* Automatically configure ``INTERNAL_IPS`` to show debug_toolbar inside contaniers when ``ENABLE_DEBUG_TOOLBAR`` is
  ``True``.
* Update security fixes in dependencies (thanks GitHub dependabot).

v0.14.3 (2020-11-05)
--------------------

* Fix encoding regression in 0.14.2.

v0.14.2 (2020-03-12)
--------------------

* Use UTF-8 encoding when logging to files.

v0.14.1 (2019-04-05)
--------------------

* Parse only the first .ini file starting from current directory (included) up to "/" (excluded).

v0.14.0 (2018-12-18)
--------------------

* Add SESSION_CACHE_XXX settings in CachesMixin to allow to configure sessions in cache.

v0.13.0 (2018-05-31)
--------------------

* Add optional LOG_FORMATTER_EXTRA_FIELDS setting.
* Add mixin for django-storages (currently only AWS S3).

v0.12.0 (2018-03-06)
--------------------

* Property to configure INTERNAL_IPS via .ini or envvar.
* Allow to override DEBUG_TOOLBAR_MIDDLEWARE in settings.

v0.11.0 (2018-02-02)
--------------------

* Support to set DATABASES OPTIONS options.
* Support to customize logger formatter class and format.

v0.10.0 (2017-11-08)
--------------------

* Add support for sass (and scss) and remove support for coffescript.

v0.9.1 (2017-11-08)
-------------------

* Don't wait for lock in Yubin.

v0.9.0 (2017-11-08)
-------------------

* Better defaults for DEFAULT_FROM_EMAIL and  EMAIL_BACKEND.

v0.8.0 (2017-09-01)
-------------------

* Add Sentry support for RQ.

v0.7.2 (2017-06-15)
-------------------

* Updated documentation and small bug fix in WhiteNoiseMixin.

v0.7.1 (2017-06-15)
-------------------

* Added documentation first version.

v0.7.0 (2017-06-12)
-------------------

* Add support for SECURE_PROXY_SSL_HEADER in SecurityMixin.

v0.6.0 (2017-05-31)
-------------------

* Breaking change: Remove DATABASE_OPTIONS, it doesn't work with environment variables.

v0.5.0 (2017-05-08)
-------------------

* Strip names and values from options.
* Add support for redis password.

v0.4.2 (2016-11-10)
-------------------

* Fix missing return in database mixin.

v0.4.1 (2016-11-04)
-------------------

* COMPRESS_CSS_HASHING_METHOD = 'content' by default.
* Accept DATABASE_OPTIONS.
* Fix #2 ImportError: cannot import name 'NoArgsCommand' with Django 1.10.


v0.4.0 (2016-08-29)
-------------------

* Support Django 1.10.
* Support django-configurations 2
* Support Babel 6.
* Add Whitenoise mixin.
* Better handling and defaults for database tests.

v0.3.0 (2016-05-31)
-------------------

* First public version.
