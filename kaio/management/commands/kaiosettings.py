# -*- coding: utf-8 -*-
# bcabezas@apsl.net

try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand

from kaio import Options


def module_to_dict(module, omittable=lambda k: k.startswith('_')):
    "Converts a module namespace to a Python dictionary. Used by get_settings_diff."
    return dict([(k, repr(v)) for k, v in module.__dict__.items() if not omittable(k)])


def clint_encode(value):
    """clint puts crashess when value is unicode. so we always encode"""
    return value


class Command(NoArgsCommand):
    help = """Displays differences between the current settings.py and Django's
    default settings. Settings that don't appear in the defaults are
    followed by "###"."""

    requires_model_validation = False

    def handle_noargs(self, **options):
        # Inspired by Postfix's "postconf -n".
        from django.conf import settings, global_settings

        # Because settings are imported lazily, we need to explicitly load them.
        settings._setup()

        user_settings = module_to_dict(settings._wrapped)
        default_settings = module_to_dict(global_settings)

        opts = Options()
        from clint.textui import puts, colored
        pformat = "%30s: %-30s %-30s %-30s"
        puts('')
        puts(pformat % (
            colored.white('Option'),
            colored.cyan('APP Value'),
            colored.cyan('INI Value'),
            colored.green('APP Default')))
        puts('')
        for section in opts.sections:
            puts(pformat % (colored.green("[%s]" % section), '', '', ''))
            for key, kaio_value in opts.items(section):
                keycolor = colored.magenta(key)
                if key in user_settings:
                    value = colored.green(user_settings[key])
                    keycolor = colored.blue(key)
                else:
                    value = colored.green(opts.options[key].get_value_or_default())

                default_value = opts.options[key].default_value
                kaio_value = kaio_value if kaio_value else repr(kaio_value)

                puts(pformat % (
                    keycolor,
                    clint_encode(value),
                    colored.white(clint_encode(kaio_value)),
                    clint_encode(default_value)))

            puts('')

        puts(colored.white("No configurables directamente en INI (estáticos o compuestos por otros):"))
        puts()

        not_configured = set(user_settings.keys()) - set(opts.keys())
        #not_configured = not_configured - set([
            #'INSTALLED_APPS',
            #'MIDDLEWARE_CLASSES',
            #'CONTEXT_PROCESSORS',
            #])
        pformat = "%30s: %-50s"
        puts(pformat % (
            colored.white('Option'),
            colored.cyan('Value')))
        for key in sorted(not_configured):
            if key not in default_settings:
                puts(pformat % (colored.blue(key),
                    user_settings[key]))
                    #'###'))
            elif user_settings[key] != default_settings[key]:
                puts(pformat % (
                    colored.blue(key),
                    colored.green(user_settings[key])))
                    #colored.white(default_settings[key])))

    def handle(self, **options):
        return self.handle_noargs(**options)
