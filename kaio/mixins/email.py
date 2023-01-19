# -*- coding: utf-8 -*-

import logging
import os
from kaio import Options
from functools import partial


logger = logging.getLogger(__name__)
opts = Options()
get = partial(opts.get, section='Email')


class EmailMixin(object):
    """Settings para enviar emails"""

    # Django settings: https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend

    @property
    def DEFAULT_FROM_EMAIL(self):
        return get('DEFAULT_FROM_EMAIL', 'Example <info@example.com>')

    @property
    def EMAIL_BACKEND(self):
        backend = get('EMAIL_BACKEND')
        if backend:
            return backend

        if 'django_yubin' not in self.INSTALLED_APPS:
            return 'django.core.mail.backends.smtp.EmailBackend'

        try:
            import django_yubin  # type: ignore  # noqa
        except ImportError:
            logger.warn('WARNING: django_yubin in INSTALLED_APPS but not pip installed.')
            return 'django.core.mail.backends.smtp.EmailBackend'

        try:
            from django_yubin.version import VERSION  # type: ignore  # noqa
            if VERSION[0] > 1:
                return 'django_yubin.backends.QueuedEmailBackend'
            else:
                return 'django_yubin.smtp_queue.EmailBackend'
        except Exception:
            return 'django_yubin.smtp_queue.EmailBackend'


    @property
    def EMAIL_FILE_PATH(self):
        return get('EMAIL_FILE_PATH', None)

    @property
    def EMAIL_HOST(self):
        return get('EMAIL_HOST', 'localhost')

    @property
    def EMAIL_HOST_PASSWORD(self):
        return get('EMAIL_HOST_PASSWORD', '')

    @property
    def EMAIL_HOST_USER(self):
        return get('EMAIL_HOST_USER', '')

    @property
    def EMAIL_PORT(self):
        return get('EMAIL_PORT', 25)

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        return get('EMAIL_SUBJECT_PREFIX', '[Django] ')

    @property
    def EMAIL_USE_TLS(self):
        return get('EMAIL_USE_TLS', False)

    # django-yubin settings: http://django-yubin.readthedocs.org/en/latest/settings.html

    @property
    def MAILER_PAUSE_SEND(self):
        return get('MAILER_PAUSE_SEND', False)

    @property
    def MAILER_USE_BACKEND(self):
        return get('MAILER_USE_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

    @property
    def MAILER_HC_QUEUED_LIMIT_OLD(self):
        return get('MAILER_HC_QUEUED_LIMIT_OLD', 30)

    @property
    def MAILER_STORAGE_BACKEND(self):
        return get('MAILER_STORAGE_BACKEND', "django_yubin.storage_backends.DatabaseStorageBackend")

    @property
    def MAILER_STORAGE_DELETE(self):
        return get('MAILER_STORAGE_DELETE', True)

    @property
    def MAILER_FILE_STORAGE_DIR(self):
        return get('MAILER_FILE_STORAGE_DIR', "yubin")


    # deprecated, for backwards compatibility

    @property
    def MAILER_MAIL_ADMINS_PRIORITY(self):
        try:
            from django_yubin import constants
            priority = constants.PRIORITY_HIGH
        except Exception:
            priority = 1
        return get('MAILER_MAIL_ADMINS_PRIORITY', priority)

    @property
    def MAILER_MAIL_MANAGERS_PRIORITY(self):
        return get('MAILER_MAIL_MANAGERS_PRIORITY', None)

    @property
    def MAILER_EMPTY_QUEUE_SLEEP(self):
        return get('MAILER_EMPTY_QUEUE_SLEEP', 30)

    @property
    def MAILER_LOCK_WAIT_TIMEOUT(self):
        return get('MAILER_LOCK_WAIT_TIMEOUT', 0)

    @property
    def MAILER_LOCK_PATH(self):
        return get("MAILER_LOCK_PATH", os.path.join(self.APP_ROOT, "send_mail"))
