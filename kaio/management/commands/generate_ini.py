# -*- coding: utf-8 -*-
# @author: bcabezas@apsl.net

import sys

from clint.textui import puts, colored
try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand

from kaio import Options


def module_to_dict(module, omittable=lambda k: k.startswith('_')):
    """
    Converts a module namespace to a Python dictionary. Used by get_settings_diff.
    """
    return dict([(k, repr(v)) for k, v in module.__dict__.items() if not omittable(k)])


class Command(NoArgsCommand):
    help = """Print a .ini with default values in stdout."""

    requires_model_validation = False

    def handle_noargs(self, **options):
        # Inspired by Postfix's "postconf -n".
        from django.conf import settings

        # Because settings are imported lazily, we need to explicitly load them.
        settings._setup()

        user_settings = module_to_dict(settings._wrapped)

        opts = Options()
        pformat = "%-25s = %s"
        puts('')
        for section in opts.sections:
            puts(colored.green("[%s]" % section))
            for key, kaio_value in opts.items(section):
                keycolor = colored.magenta(key)
                if key in user_settings:
                    keycolor = colored.blue(key)

                default_value = opts.options[key].default_value
                value = kaio_value or default_value

                if sys.version_info[0] < 3:
                    value = unicode(value).encode('utf8')
                else:
                    value = str(value)

                try:
                    puts(pformat % (keycolor, value))
                except Exception as e:
                    raise e
            puts('')

    def handle(self, **options):
        return self.handle_noargs(**options)
