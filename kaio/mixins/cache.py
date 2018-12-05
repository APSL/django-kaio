# -*- coding: utf-8 -*-

from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Cache')


class CachesMixin(object):

    # Settings for default cache.

    @property
    def CACHE_TYPE(self):
        return get('CACHE_TYPE', 'locmem')

    @property
    def REDIS_HOST(self):
        return get('REDIS_HOST', 'localhost')

    @property
    def REDIS_PORT(self):
        return get('REDIS_PORT', 6379)

    @property
    def CACHE_REDIS_DB(self):
        return get('CACHE_REDIS_DB', 2)

    @property
    def CACHE_REDIS_PASSWORD(self):
        return get('CACHE_REDIS_PASSWORD', None)

    @property
    def CACHE_PREFIX(self):
        return get('CACHE_PREFIX', self.APP_SLUG)

    @property
    def CACHE_TIMEOUT(self):
        return get('CACHE_TIMEOUT', 3600)

    @property
    def CACHE_MAX_ENTRIES(self):
        return get('CACHE_MAX_ENTRIES', 10000)

    @property
    def DEFAULT_CACHE(self):
        if self.CACHE_TYPE == 'redis':
            CACHE = {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION':  'redis://%s:%s/%s' % (self.REDIS_HOST,
                                                   self.REDIS_PORT,
                                                   self.CACHE_REDIS_DB),
                'KEY_PREFIX': self.CACHE_PREFIX,
                'TIMEOUT': self.CACHE_TIMEOUT,
                'OPTIONS': {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    'MAX_ENTRIES': self.CACHE_MAX_ENTRIES,
                },
            }
            if self.CACHE_REDIS_PASSWORD is not None:
                CACHE['OPTIONS']['PASSWORD'] = self.CACHE_REDIS_PASSWORD
        elif self.CACHE_TYPE == 'locmem':
            CACHE = {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'CACHE_PREFIX': self.CACHE_PREFIX,
                'LOCATION': 'unique-key-apsl'
            }
        else:
            CACHE = {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }

        return CACHE

    # Settings for session cache.
    # You must set SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    # (or cached_db). By default use almost same settings as default cache.

    @property
    def SESSION_CACHE_TYPE(self):
        return get('SESSION_CACHE_TYPE', self.CACHE_TYPE)

    @property
    def SESSION_REDIS_HOST(self):
        return get('SESSION_REDIS_HOST', self.REDIS_HOST)

    @property
    def SESSION_REDIS_PORT(self):
        return get('SESSION_REDIS_PORT', self.REDIS_PORT)

    @property
    def SESSION_CACHE_REDIS_DB(self):
        return get('SESSION_CACHE_REDIS_DB', 3)

    @property
    def SESSION_CACHE_REDIS_PASSWORD(self):
        return get('SESSION_CACHE_REDIS_PASSWORD', self.CACHE_REDIS_PASSWORD)

    @property
    def SESSION_CACHE_PREFIX(self):
        return get('SESSION_CACHE_PREFIX', '%s_session' % self.CACHE_PREFIX)

    @property
    def SESSION_CACHE_TIMEOUT(self):
        return get('SESSION_CACHE_TIMEOUT', None)

    @property
    def SESSION_CACHE_MAX_ENTRIES(self):
        return get('SESSION_CACHE_MAX_ENTRIES', 1000000)

    @property
    def SESSION_CACHE(self):
        # Support for Redis only
        if self.SESSION_CACHE_TYPE != 'redis' or self.SESSION_ENGINE not in (
                'django.contrib.sessions.backends.cache',
                'django.contrib.sessions.backends.cached_db'):
            return

        CACHE = {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION':  'redis://%s:%s/%s' % (self.SESSION_REDIS_HOST,
                                               self.SESSION_REDIS_PORT,
                                               self.SESSION_CACHE_REDIS_DB),
            'KEY_PREFIX': self.SESSION_CACHE_PREFIX,
            'TIMEOUT': self.SESSION_CACHE_TIMEOUT,
            'OPTIONS': {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                'MAX_ENTRIES': self.SESSION_CACHE_MAX_ENTRIES,
            },
        }

        if self.SESSION_CACHE_REDIS_PASSWORD is not None:
            CACHE['OPTIONS']['PASSWORD'] = self.SESSION_CACHE_REDIS_PASSWORD

        return CACHE

    @property
    def SESSION_CACHE_ALIAS(self):
        return get('SESSION_CACHE_ALIAS', 'session')

    # Main cache settings.

    @property
    def CACHES(self):
        caches = {'default': self.DEFAULT_CACHE}
        session_cache = self.SESSION_CACHE
        if session_cache:
            caches[self.SESSION_CACHE_ALIAS] = session_cache
        return caches
