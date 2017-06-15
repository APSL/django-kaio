# encoding: utf-8

from functools import partial

from kaio import Options


opts = Options()
get = partial(opts.get, section='WhiteNoise')


class WhiteNoiseMixin(object):
    """Settings for http://whitenoise.evans.io version 3"""

    @property
    def ENABLE_WHITENOISE(self):
        enabled = get('ENABLE_WHITENOISE', False)
        if enabled:
            try:
                import whitenoise
                self._add_whitenoise_to_installed_apps()
                self._add_whitenoise_to_middleware()
            except ImportError:
                return False
        return enabled

    @property
    def WHITENOISE_AUTOREFRESH(self):
        return get('WHITENOISE_AUTOREFRESH', True)

    @property
    def WHITENOISE_USE_FINDERS(self):
        return get('WHITENOISE_USE_FINDERS', True)

    def _add_whitenoise_to_installed_apps(self):
        if 'whitenoise.runserver_nostatic' not in self.INSTALLED_APPS:
            index = self.INSTALLED_APPS.index('django.contrib.staticfiles')
            self.INSTALLED_APPS.insert(index, 'whitenoise.runserver_nostatic')

    def _add_whitenoise_to_middleware(self):
        middlewares_settings = (
            'MIDDLEWARE',  # django >= 1.10
            'MIDDLEWARE_CLASSES',  # django < 1.10
        )
        for middleware_setting in middlewares_settings:
            middlewares = getattr(self, middleware_setting, None)
            if middlewares is not None:
                if 'whitenoise.middleware.WhiteNoiseMiddleware' not in middlewares:
                    try:
                        index = middlewares.index('django.middleware.security.SecurityMiddleware') + 1
                    except ValueError:
                        index = 0
                    middlewares.insert(index, 'whitenoise.middleware.WhiteNoiseMiddleware')
