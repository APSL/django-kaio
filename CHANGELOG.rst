==========
Change log
==========

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
