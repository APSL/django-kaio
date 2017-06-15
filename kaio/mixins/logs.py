# -*- coding: utf-8 -*-

from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Logs')


class LogsMixin(object):
    """Django Logging configuration"""

    @property
    def LOG_LEVEL(self):
        return get('LOG_LEVEL', 'DEBUG').upper()

    @property
    def DJANGO_LOG_LEVEL(self):
        return get('DJANGO_LOG_LEVEL', 'ERROR').upper()

    @property
    def LOG_FILE(self):
        return get('LOG_FILE', '')

    @property
    def EXTRA_LOGGING(self):
        """
        lista modulos con los distintos niveles a logear y su
        nivel de debug

        Por ejemplo:

            [Logs]
            EXTRA_LOGGING = oscar.paypal:DEBUG, django.db:INFO

        """

        input_text = get('EXTRA_LOGGING', '')
        modules = input_text.split(',')
        if input_text:
            modules = input_text.split(',')
            modules = [x.split(':') for x in modules]
        else:
            modules = []
        return modules

    @property
    def SENTRY_ENABLED(self):
        enabled = get('SENTRY_ENABLED', False)
        if enabled:
            try:
                import raven
                self.add_sentry_to_installed_apps()
            except ImportError:
                return False
        return enabled

    @property
    def SENTRY_DSN(self):
        return get('SENTRY_DSN', '')

    # The best way to propagate logs up to the root logger is to prevent
    # Django logging configuration and handle it ourselves.
    #
    # http://stackoverflow.com/questions/20282521/django-request-logger-not-propagated-to-root/22336174#22336174
    # https://docs.djangoproject.com/en/1.10/topics/logging/#disabling-logging-configuration
    LOGGING_CONFIG = None

    @property
    def LOGGING(self):
        config = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': self.formatters,
            'filters': self.filters,
            'handlers': self.handlers,
            'loggers': self.loggers,
        }
        import logging.config
        logging.config.dictConfig(config)
        return config

    @property
    def handlers(self):
        handlers = {}

        handlers['default'] = {
            'level': self.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'apsldefault'
        }

        if self.LOG_FILE:
            handlers['default']['class'] = 'logging.FileHandler'
            handlers['default']['filename'] = self.LOG_FILE

        handlers['mail_admins'] = {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }

        if self.SENTRY_ENABLED:
            handlers['sentry'] = {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            }

        return handlers

    @property
    def loggers(self):
        loggers = {}

        loggers[''] = {
            'handlers': ['default'],
            'level': self.LOG_LEVEL,
            'propagate': True,
        }

        loggers['rq.worker'] = {
            'handlers': ['default'],
            'level': self.LOG_LEVEL,
            'propagate': False,
        }

        loggers['requests.packages.urllib3'] = {
            'handlers': ['default'],
            'level': self.LOG_LEVEL,
            'propagate': False,
        }

        loggers['django'] = {
            'handlers': ['default'],
            'level': self.DJANGO_LOG_LEVEL,
            'propagate': False,
        }

        if self.EXTRA_LOGGING:
            try:
                for module, level in self.EXTRA_LOGGING:
                    loggers[module] = {
                        'handlers': ['default'],
                        'level': level,
                        'propagate': False,
                    }
            except Exception as exc:
                import sys
                sys.stderr.write(exc)

        if self.SENTRY_ENABLED:
            loggers['']['handlers'].append('sentry')
            loggers['django']['handlers'].append('sentry')
            loggers['raven'] = {
                'handlers': ['default'],
                'level': self.LOG_LEVEL,
                'propagate': False,
            }
            loggers['sentry.errors'] = {
                'handlers': ['default'],
                'level': self.LOG_LEVEL,
                'propagate': False,
            }
        else:
            loggers['raven'] = {
                'handlers': ['default'],
                'level': 'WARNING',
            }

        return loggers

    @property
    def formatters(self):
        return {
            'apsldefault': {
                'format': "[%(asctime)s] %(levelname)s %(name)s-%(lineno)s %(message)s"
            }
        }

    @property
    def filters(self):
        return {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        }

    def add_sentry_to_installed_apps(self):
        if 'raven.contrib.django.raven_compat' not in self.INSTALLED_APPS:
            self.INSTALLED_APPS.append('raven.contrib.django.raven_compat')
