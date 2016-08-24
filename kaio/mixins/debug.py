# -*- coding: utf-8 -*-

from functools import partial

from kaio import Options


opts = Options()
get = partial(opts.get, section='Debug')


class DebugMixin(object):
    """Securty base settings"""

    # https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#explicit-setup
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    INTERNAL_IPS = ['127.0.0.1']

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
        hosts = get('ALLOWED_HOSTS')
        return [h.strip() for h in hosts.split(',') if h]

    def add_to_installed_apps(self):
        if 'debug_toolbar' not in self.INSTALLED_APPS:
            self.INSTALLED_APPS.append('debug_toolbar')

    def add_to_middleware_classes(self):
        if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in self.MIDDLEWARE:
            self.MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
