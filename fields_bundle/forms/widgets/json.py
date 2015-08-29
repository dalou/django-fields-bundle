import re
import os
import logging

from django.conf import settings
from django import forms
from django.template import Context

from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt


logger = logging.getLogger(__name__)

class JSONInput(forms.widgets.TextInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.

    template_name = 'cargo/forms/widgets/file_input.html'

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)

        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': True,
            'mask': True
            #'format': 'd.m.Y'
        })
        super(JSONInput, self).__init__(*args, **kwargs)

