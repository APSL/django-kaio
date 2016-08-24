# -*- coding: utf-8 -*-

from os.path import join, abspath
from kaio import Options
from configurations import Configuration
from functools import partial

opts = Options()
get = partial(opts.get, section='Filer')

class FilerMixin(object):
    """Settings para django-filer y easy_thumbnails"""

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        # 'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )

    @property
    def FILER_IS_PUBLIC_DEFAULT(self):
        return get('FILER_IS_PUBLIC_DEFAULT', True)

    @property
    def FILER_ENABLE_PERMISSIONS(self):
        return get('FILER_ENABLE_PERMISSIONS', False)

    @property
    def FILER_DEBUG(self):
        return get('FILER_DEBUG', False)

    @property
    def FILER_ENABLE_LOGGING(self):
        return get('FILER_ENABLE_LOGGING', False)

    @property
    def FILER_0_8_COMPATIBILITY_MODE(self):
        get('FILER_0_8_COMPATIBILITY_MODE', False)

    @property
    def THUMBNAIL_DEBUG(self):
        return get('THUBMNAIL_DEBUG', False)

    @property
    def THUMBNAIL_QUALITY(self):
        return get('THUMBNAIL_QUALITY', 85)

    @property
    def FILER_CUSTOM_NGINX_SERVER(self):
        """If true will serve secure file trough XNginxXAccelRedirectServer"""
        return get('FILER_CUSTOM_NGINX_SERVER', False)

    @property
    def default_file_storage(self):
        """Common storage for filer configs"""
        return getattr(
            Configuration, 'DEFAULT_FILE_STORAGE',
            'django.core.files.storage.FileSystemStorage')

    @property
    def FILER_CUSTOM_SECURE_MEDIA_ROOT(self):
        """Secure media root
        As in filer settings, defaults to MEDIA_ROOT/../smedia"""
        return opts.get(
            'FILER_CUSTOM_SECURE_MEDIA_ROOT',
            abspath(join(self.MEDIA_ROOT, '..', 'smedia')))

    @property
    def filer_private_files_path(self):
        return abspath(
            join(
                self.FILER_CUSTOM_SECURE_MEDIA_ROOT,
                'filer_private'
            ))

    @property
    def filer_private_thumbnails_path(self):
        return abspath(
            join(
                self.FILER_CUSTOM_SECURE_MEDIA_ROOT,
                'filer_private_thumbnails'))

    @property
    def FILER_SERVERS(self):
        """Filer config to be served from XNginxXAccelRedirectServer
        see http://django-filer.readthedocs.org/en/0.9.4/secure_downloads.html#secure-downloads
        """
        if not self.FILER_CUSTOM_NGINX_SERVER:
            return {}
        else:
            return {
                'private': {
                    'main': {
                        'ENGINE': 'filer.server.backends.nginx.NginxXAccelRedirectServer',
                        'OPTIONS': {
                            'location': self.filer_private_files_path,
                            'nginx_location': '/nginx_filer_private',
                        },
                    },
                    'thumbnails': {
                        'ENGINE': 'filer.server.backends.nginx.NginxXAccelRedirectServer',
                        'OPTIONS': {
                            'location': self.filer_private_thumbnails_path,
                            'nginx_location': '/nginx_filer_private_thumbnails',
                        },
                    },
                },
            }

    @property
    def FILER_STORAGES(self):
        """Filer config to set custom private media path
        http://django-filer.readthedocs.org/en/0.9.4/settings.html#filer-storages
        """
        if not self.FILER_CUSTOM_NGINX_SERVER:
            return {}

        return {
            'public': {
                'main': {
                    'ENGINE': self.default_file_storage,
                    'OPTIONS': {},
                    'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
                    'UPLOAD_TO_PREFIX': 'filer_public',
                },
                'thumbnails': {
                    'ENGINE': self.default_file_storage,
                    'OPTIONS': {},
                    'THUMBNAIL_OPTIONS': {
                        'base_dir': 'filer_public_thumbnails',
                    },
                },
            },
            'private': {
                'main': {
                    'ENGINE': 'filer.storage.PrivateFileSystemStorage',
                    'OPTIONS': {
                        'location': self.filer_private_files_path,
                        'base_url': '/smedia/filer_private/',
                    },
                    'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
                    'UPLOAD_TO_PREFIX': '',
                },
                'thumbnails': {
                    'ENGINE': 'filer.storage.PrivateFileSystemStorage',
                    'OPTIONS': {
                        'location': self.filer_private_thumbnails_path,
                        'base_url': '/smedia/filer_private_thumbnails/',
                    },
                    'THUMBNAIL_OPTIONS': {},
                },
            },
        }
