# -*- coding: utf-8 -*-

from kaio import Options
from functools import partial

opts = Options()

get = partial(opts.get, section='Debug')

class DebugMixin(object):
    """Securty base settings"""

    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    INTERNAL_IPS = ('127.0.0.1', )

    @property
    def DEBUG(self):
        return get('DEBUG', False)

    @property
    def TEMPLATE_DEBUG(self):
        for template in self.TEMPLATES:
            if template['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
                template['OPTIONS']['debug'] = get('TEMPLATE_DEBUG', self.DEBUG)

    @property
    def ENABLE_DEBUG_TOOLBAR(self):
        enabled = get('ENABLE_DEBUG_TOOLBAR', self.DEBUG)
        if enabled:
            try:
                import debug_toolbar
            except ImportError:
                return False
            else:
                self.add_to_installed_apps()
                self.add_to_middleware_classes()

        return enabled

    @property
    def ALLOWED_HOSTS(self):
        hosts = get('ALLOWED_HOSTS', 'www.change-me.net')
        return [h.strip() for h in hosts.split(',')]

    def add_to_installed_apps(self):
        if 'debug_toolbar' not in self.INSTALLED_APPS:
            self.INSTALLED_APPS += ('debug_toolbar', )

    def add_to_middleware_classes(self):
        if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in self.MIDDLEWARE_CLASSES:
            self.MIDDLEWARE_CLASSES += (
                'debug_toolbar.middleware.DebugToolbarMiddleware',
            )
