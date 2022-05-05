from kaio import Options
from functools import partial


opts = Options()
get = partial(opts.get, section='Sentry')


class SentryMixin(object):
    """Sentry configuration"""

    @property
    def SENTRY_DSN(self):
        dsn = get('SENTRY_DSN')
        if dsn:
            self.sentry_init(dsn)
        return dsn

    def sentry_init(self, dsn):
        import sentry_sdk
        sentry_sdk.init(
            dsn=dsn,
            integrations=self.integrations(),
            send_default_pii=True,  # Associate Django user.id or user's IP to errors
        )

    def integrations(self):
        from sentry_sdk.integrations.django import DjangoIntegration
        return [DjangoIntegration()]
