# -*- coding: utf-8 -*-

from functools import partial

from kaio import Options


opts = Options()
get = partial(opts.get, section='Debug')


class DebugMixin(object):
    """Debug base settings"""

    @property
    def DEBUG(self):
        return get('DEBUG', False)

    @property
    def TEMPLATE_DEBUG(self):
        debug = get('TEMPLATE_DEBUG', self.DEBUG)
        for template in self.TEMPLATES:
            if template['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
                template['OPTIONS']['debug'] = debug

    # https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#explicit-setup
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    DEBUG_TOOLBAR_MIDDLEWARE = 'debug_toolbar.middleware.DebugToolbarMiddleware'

    @property
    def ENABLE_DEBUG_TOOLBAR(self):
        enabled = get('ENABLE_DEBUG_TOOLBAR', self.DEBUG)
        if enabled:
            try:
                import debug_toolbar
            except ImportError:
                return False
            else:
                self._add_debug_toolbar_to_installed_apps()
                self._add_debug_toolbar_to_middleware()

        return enabled

    @property
    def INTERNAL_IPS(self):
        ips = [ip.strip() for ip in get('INTERNAL_IPS', '127.0.0.1').split(',') if ip]
        return ips

    def _add_debug_toolbar_to_installed_apps(self):
        if 'debug_toolbar' not in self.INSTALLED_APPS:
            self.INSTALLED_APPS.append('debug_toolbar')

    def _add_debug_toolbar_to_middleware(self):
        middlewares_settings = (
            'MIDDLEWARE',  # django >= 1.10
            'MIDDLEWARE_CLASSES',  # django < 1.10
        )
        for middleware_setting in middlewares_settings:
            middlewares = getattr(self, middleware_setting, None)
            if middlewares is not None:
                if self.DEBUG_TOOLBAR_MIDDLEWARE not in middlewares:
                    middlewares.insert(0, self.DEBUG_TOOLBAR_MIDDLEWARE)
