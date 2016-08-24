# -*- coding: utf-8 -*-

from configurations import Configuration
from kaio import Options
from functools import partial

opts = Options()
get = partial(opts.get, section='Compress')


class CompressMixin(object):

    # COMPRESS_PARSER = 'compressor.parser.LxmlParser'
    COMPRESS_CSS_FILTER = [
        'compressor.filters.css_default.CssAbsoluteFilter',
    ]
    STATICFILES_FINDERS = list(Configuration.STATICFILES_FINDERS) + [
        "compressor.finders.CompressorFinder",
    ]

    @property
    def COMPRESS_ENABLED(self):
        return get('COMPRESS_ENABLED', False)

    @property
    def COMPRESS_LESSC_ENABLED(self):
        return get('COMPRESS_LESSC_ENABLED', True)

    @property
    def COMPRESS_COFFEE_ENABLED(self):
        return get('COMPRESS_COFFEE_ENABLED', False)

    @property
    def COMPRESS_BABEL_ENABLED(self):
        return get('COMPRESS_BABEL_ENABLED', False)

    @property
    def COMPRESS_PRECOMPILERS(self):
        precompilers = []
        if self.COMPRESS_LESSC_ENABLED:
            precompilers.append(('text/less', 'lessc {infile} {outfile}'))
        if self.COMPRESS_COFFEE_ENABLED:
            precompilers.append(('text/coffeescript', 'coffee --compile --stdio'))
        if self.COMPRESS_BABEL_ENABLED:
            precompilers.append((
                'text/babel',
                'babel {infile} -o {outfile} --modules ignore --source-maps inline'
            ))
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
