# -*- coding: utf-8 -*-

from configurations import Configuration
from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Compress')


class CompressMixin(object):

    STATICFILES_FINDERS = list(Configuration.STATICFILES_FINDERS) + [
        "compressor.finders.CompressorFinder",
    ]

    @property
    def COMPRESS_ENABLED(self):
        return get('COMPRESS_ENABLED', False)

    @property
    def COMPRESS_CSS_HASHING_METHOD(self):
        return get('COMPRESS_CSS_HASHING_METHOD', 'content')

    @property
    def COMPRESS_DEBUG_TOGGLE(self):
        if self.DEBUG:
            return 'nocompress'
        return None

    @property
    def COMPRESS_LESSC_ENABLED(self):
        return get('COMPRESS_LESSC_ENABLED', True)

    @property
    def COMPRESS_BABEL_ENABLED(self):
        return get('COMPRESS_BABEL_ENABLED', True)

    @property
    def COMPRESS_COFFEE_ENABLED(self):
        return get('COMPRESS_COFFEE_ENABLED', False)

    @property
    def COMPRESS_LESSC_PATH(self):
        return get('COMPRESS_LESSC_PATH', 'lessc')

    @property
    def COMPRESS_BABEL_PATH(self):
        return get('COMPRESS_BABEL_PATH', 'babel')

    @property
    def COMPRESS_COFEE_PATH(self):
        return get('COMPRESS_COFEE_PATH', 'coffee')

    @property
    def COMPRESS_PRECOMPILERS(self):
        precompilers = []
        if self.COMPRESS_LESSC_ENABLED:
            precompilers.append(('text/less', self.COMPRESS_LESSC_PATH + ' {infile} {outfile}'))
        if self.COMPRESS_BABEL_ENABLED:
            precompilers.append(('text/babel', self.COMPRESS_BABEL_PATH + ' {infile} -o {outfile}'))
        if self.COMPRESS_COFFEE_ENABLED:
            precompilers.append(('text/coffeescript', self.COMPRESS_COFFEE_PATH + ' --compile --stdio'))
        return precompilers

    # offline settings
    # http://django-compressor.readthedocs.org/en/latest/settings/#offline-settings

    @property
    def COMPRESS_OFFLINE(self):
        return get('COMPRESS_OFFLINE', False)

    @property
    def COMPRESS_OFFLINE_TIMEOUT(self):
        return get('COMPRESS_OFFLINE_TIMEOUT', 31536000)  # 1 year in seconds

    @property
    def COMPRESS_OFFLINE_MANIFEST(self):
        return get('COMPRESS_OFFLINE_MANIFEST', 'manifest.json')

    def COMPRESS_OUTPUT_DIR(self):
        if not self.COMPRESS_ENABLED and self.COMPRESS_LESSC_ENABLED:
            return ''
        else:
            return get('COMPRESS_OUTPUT_DIR', 'CACHE/')
