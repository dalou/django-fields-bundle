import re
import os
import logging, json, random

from django.conf import settings
from django import forms
from django.template import Context

from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt


logger = logging.getLogger(__name__)

class LocationInput(forms.widgets.TextInput):


    class Media:
        # css = {
        #     'all': (settings.STATIC_URL + 'vendors/croppable/jquery.datetimepicker.css')
        # }
        js = (settings.STATIC_URL + 'cargo/forms/geo_location.js',
            'https://maps.googleapis.com/maps/api/js?libraries=geometry&v=3.exp&sensor=true', )


    template_name = 'cargo/forms/widgets/_geo_location_input.html'

    def __init__(self, *args, **kwargs):

        options = kwargs.pop('options', {

        })
        super(LocationInput, self).__init__(*args, **kwargs)


    def render(self, name, value, attrs=None):

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
             # Only add the 'value' attribute if a value is non-empty.
             final_attrs['value'] = force_unicode(self._format_value(value))

        #print name, attrs, final_attrs

        inputs_prefix_id = final_attrs['id'].replace('original_address', '')

        return render_to_string(self.template_name, Context({
            'inputs_prefix_id': inputs_prefix_id,
            'input_attrs': flatatt(final_attrs),
            'value': value if value else '',
            'attr_id': random.getrandbits(128),#"%s-field" % final_attrs['id'],
            'input_id': final_attrs['id'],
        }))
