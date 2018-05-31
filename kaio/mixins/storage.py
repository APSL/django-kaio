# -*- coding: utf-8 -*-

from functools import partial

from kaio import Options


opts = Options()
get = partial(opts.get, section='Storage')


class StorageMixin(object):
    """Settings for django-storages

    Currently only supports AWS S3.
    """

    # AWS S3 settings: http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

    @property
    def DEFAULT_FILE_STORAGE(self):
        return get('DEFAULT_FILE_STORAGE', 'storages.backends.s3boto3.S3Boto3Storage')

    @property
    def AWS_S3_SIGNATURE_VERSION(self):
        return get('AWS_S3_SIGNATURE_VERSION', 's3v4')

    @property
    def AWS_S3_REGION_NAME(self):
        return get('AWS_S3_REGION_NAME', None)

    @property
    def AWS_STORAGE_BUCKET_NAME(self):
        return get('AWS_STORAGE_BUCKET_NAME', '')

    @property
    def AWS_LOCATION(self):
        return get('AWS_LOCATION', '')

    @property
    def AWS_ACCESS_KEY_ID(self):
        return get('AWS_ACCESS_KEY_ID', '')

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return get('AWS_SECRET_ACCESS_KEY', '')

    @property
    def AWS_QUERYSTRING_AUTH(self):
        return get('AWS_QUERYSTRING_AUTH', True)

    @property
    def AWS_DEFAULT_ACL(self):
        return get('AWS_DEFAULT_ACL', 'private')
