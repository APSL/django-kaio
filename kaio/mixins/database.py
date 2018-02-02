# -*- coding: utf-8 -*-

from functools import partial
from kaio import Options


opts = Options()
get = partial(opts.get, section='Database')


class DatabasesMixin(object):

    @staticmethod
    def get_engine(prefix):
        """
        Retrieve the database engine.
        Only change the full engine string if there is no «backends» in it.
        """
        engine = get('{}DATABASE_ENGINE'.format(prefix), 'sqlite3')
        if 'backends' in engine:
            return engine
        return 'django.db.backends.' + engine

    def get_databases(self, prefix=''):
        databases = {
            'default': {
                'ENGINE': self.get_engine(prefix),
                'NAME': get('{}DATABASE_NAME'.format(prefix), '{}db.sqlite'.format(prefix.lower())),
                'USER': get('{}DATABASE_USER'.format(prefix), None),
                'PASSWORD': get('{}DATABASE_PASSWORD'.format(prefix), ''),
                'HOST': get('{}DATABASE_HOST'.format(prefix), ''),
                'PORT': get('{}DATABASE_PORT'.format(prefix), ''),
                'CONN_MAX_AGE': get('{}DATABASE_CONN_MAX_AGE'.format(prefix), 0),
                'TEST': {
                    'NAME': get('{}DATABASE_NAME'.format(prefix), None),
                }
            }
        }

        options = get('DATABASE_OPTIONS_OPTIONS')
        if options:
            databases['default']['OPTIONS'] = {'options': options}

        return databases

    def DATABASES(self):
        return self.get_databases()
