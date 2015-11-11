import os
from django.conf import settings
from django.contrib.staticfiles import finders

FIELDS_BUNDLE_TINYMCE_URL = getattr(settings, 'FIELDS_BUNDLE_TINYMCE_URL', "//tinymce.cachefly.net/4.2/tinymce.min.js")

FIELDS_BUNDLE_TINYMCE_DEFAULT_CONFIG = getattr(settings, 'FIELDS_BUNDLE_TINYMCE_DEFAULT_CONFIG',
    {
        'theme': "simple",
        'relative_urls': False
    }
)