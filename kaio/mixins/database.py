# -*- coding: utf-8 -*-

from functools import partial
from kaio import Options


opts = Options()
get = partial(opts.get, section='Database')


class DatabasesMixin(object):

    def get_engine(self, prefix):
        """
        Retrieve the database engine.
        Only change the full engine string if there is no «backends» in it.
        """
        engine = get('{}DATABASE_ENGINE'.format(prefix), 'sqlite3')
        if 'backends' in engine:
            return engine
        return 'django.db.backends.' + engine

    def get_options(self):
        options = {}
        for key in opts.keys():
            if 'DATABASE_OPTIONS_' in key.upper():
                options[str(key.split('DATABASE_OPTIONS_')[1].lower())] = get(key)
        return options

    def get_databases(self, prefix=''):
        return {
            'default': {
                'ENGINE': self.get_engine(prefix),
                'NAME': get('{}DATABASE_NAME'.format(prefix), '{}db.sqlite'.format(prefix.lower())),
                'USER': get('{}DATABASE_USER'.format(prefix), None),
                'PASSWORD': get('{}DATABASE_PASSWORD'.format(prefix), ''),
                'HOST': get('{}DATABASE_HOST'.format(prefix), ''),
                'PORT': get('{}DATABASE_PORT'.format(prefix), ''),
                'CONN_MAX_AGE': get('{}DATABASE_CONN_MAX_AGE'.format(prefix), 0),
                'OPTIONS': self.get_options(),
                'TEST': {
                    'NAME': get('{}DATABASE_NAME'.format(prefix), None),
                }
            }
        }

    def DATABASES(self):
        return self.get_databases()
