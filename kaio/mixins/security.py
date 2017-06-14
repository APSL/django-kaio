# -*- coding: utf-8 -*-

from kaio import Options

opts = Options()


def get(value, default):
    return opts.get(value, default, section='Security')


class SecurityMixin(object):
    """
    Security base settings
    """

    @property
    def SECRET_KEY(self):
        return get('SECRET_KEY', u'sysadmin, change the secret key!!!!')

    @property
    def ALLOWED_HOSTS(self):
        return [h.strip() for h in get('ALLOWED_HOSTS', '*').split(',')]

    @property
    def SECURE_PROXY_SSL_HEADER_NAME(self):
        return get('SECURE_PROXY_SSL_HEADER_NAME', 'HTTP_X_FORWARDED_PROTO')

    @property
    def SECURE_PROXY_SSL_HEADER_VALUE(self):
        return get('SECURE_PROXY_SSL_HEADER_VALUE', 'https')

    @property
    def SECURE_PROXY_SSL_HEADER(self):
        # required in order to have the request.is_secure() method to work properly in https environments
        # https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header
        # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
        return self.SECURE_PROXY_SSL_HEADER_NAME, self.SECURE_PROXY_SSL_HEADER_VALUE
