# -*- coding: utf-8 -*-

from kaio import Options
from os.path import abspath, join
from functools import partial

opts = Options()
get = partial(opts.get, section='Paths')


class PathsMixin(object):

    @property
    def APP_ROOT(self):
        return get('APP_ROOT', abspath('.'))

    @property
    def MEDIA_ROOT(self):
        return get('MEDIA_ROOT', abspath(join(self.APP_ROOT, 'media')))

    @property
    def STATIC_URL(self):
        return get('STATIC_URL', '/static/')

    @property
    def MEDIA_URL(self):
        return get('MEDIA_URL', '/media/')

    @property
    def STATIC_ROOT(self):
        return get(
            'STATIC_ROOT',
            abspath(join("/tmp", "%s-static" % self.APP_SLUG)))
