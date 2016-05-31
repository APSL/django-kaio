# -*- coding: utf-8 -*-

from kaio import Options

opts = Options()


def get(value, default):
    return opts.get(value, default, section='Security')


class SecurityMixin(object):
    """Securty base settings"""

    @property
    def SECRET_KEY(self):
        return get('SECRET_KEY', u'sysadmin, canvia la secret key!!!!')

    @property
    def ALLOWED_HOSTS(self):
        return [h.strip() for h in \
                get('ALLOWED_HOSTS', '*').split(',')]

