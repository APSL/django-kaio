# -*- coding: utf-8 -*-

from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Cache')


class CachesMixin(object):

    @property
    def REDIS_HOST(self):
        return get('REDIS_HOST', 'localhost')

    @property
    def REDIS_PORT(self):
        return get('REDIS_PORT', 6379)

    @property
    def CACHES(self):
        CACHE_TYPE = get('CACHE_TYPE', 'locmem')
        CACHE_REDIS_DB = get('CACHE_REDIS_DB', 2)
        CACHE_REDIS_PASSWORD = get('CACHE_REDIS_PASSWORD', None)
        CACHE_PREFIX = get('CACHE_PREFIX', self.APP_SLUG)
        CACHE_TIMEOUT = get('CACHE_TIMEOUT', 3600)
        CACHE_MAX_ENTRIES = get('CACHE_MAX_ENTRIES', 10000)

        if CACHE_TYPE == 'redis':
            CACHE = {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION':  'redis://%s:%s/%s' % (self.REDIS_HOST, self.REDIS_PORT, CACHE_REDIS_DB),
                'KEY_PREFIX': CACHE_PREFIX,
                'TIMEOUT': CACHE_TIMEOUT,
                'OPTIONS': {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    'MAX_ENTRIES': CACHE_MAX_ENTRIES,
                },
            }
            if CACHE_REDIS_PASSWORD is not None:
                CACHE['OPTIONS']['PASSWORD'] = CACHE_REDIS_PASSWORD
        elif CACHE_TYPE == 'locmem':
            CACHE = {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'CACHE_PREFIX': CACHE_PREFIX,
                'LOCATION': 'unique-key-apsl'
            }
        else:
            CACHE = {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }

        return {'default': CACHE}
