# -*- coding: utf-8 -*-

from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Database')

class DatabasesMixin(object):

    def DATABASES(self):
        engine = get('DATABASE_ENGINE', 'sqlite3')
        if 'django.db.backends' in engine:
            ENGINE = engine
        else:
            ENGINE = 'django.db.backends.' + engine

        return {
            'default': {
                'ENGINE': ENGINE,
                'NAME': get('DATABASE_NAME', 'db.sqlite'),
                'USER': get('DATABASE_USER', None),
                'PASSWORD': get('DATABASE_PASSWORD', ''),
                'HOST': get('DATABASE_HOST', ''),
                'PORT': get('DATABASE_PORT', ''),
                'OPTIONS': {},
            }
        }
