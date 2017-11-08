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

        backend = 'django.core.mail.backends.smtp.EmailBackend'
        if 'django_yubin' in self.INSTALLED_APPS:
            try:
                import django_yubin
                backend = 'django_yubin.smtp_queue.EmailBackend'
            except ImportError:
                logger.warn('WARNING: django_yubin in INSTALLED_APPS but not pip installed.')
        return backend

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
