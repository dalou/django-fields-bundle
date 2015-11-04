# encoding: utf-8

import re
import os
import logging

from django.conf import settings
from django import forms
from django.template import Context
from django.forms.widgets import FILE_INPUT_CONTRADICTION, CheckboxInput, FileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.utils import flatatt
from django.core.files.uploadedfile import InMemoryUploadedFile
try:
    from sorl.thumbnail.shortcuts import get_thumbnail
except:
    def get_thumbnail(image_url, *args, **kwargs):
        return image_url

logger = logging.getLogger(__name__)




class MediaInput(forms.widgets.ClearableFileInput):
    template_name = 'fields_bundle/_media_input.html'
    # class Media:
    #     css = {
    #         'all': (
    #             # settings.STATIC_URL + 'fields_bundle/image_cropped.css',
    #         )
    #     }
    #     js = (
    #         # settings.STATIC_URL + 'fields_bundle/image_cropped.js',
    #         # settings.STATIC_URL + 'js/cropper.js',
    #     )


    def __init__(self, *args, **kwargs):
        self.authorized_types = []
        if kwargs.get('authorized_types'):
            self.authorized_types = kwargs.pop('authorized_types')
        super(MediaInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        field = super(MediaInput, self).render(name, value, attrs=attrs)

        in_memory = False

        if isinstance(value, InMemoryUploadedFile):
            in_memory = True

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)
        context = {
            'only_file': len(self.authorized_types) == 1 and 'image' in self.authorized_types,
            'required': self.is_required,
            'field': field,
            'name': name,
            'value': value,
            'id': final_attrs['id'],
            'final_attrs': flatatt(final_attrs),
        }
        if not self.is_required:
            context['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
        return render_to_string(self.template_name, Context(context))

    def value_from_datadict(self, data, files, name):
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):
            return False
        print data, files
        if files:
            return files.get(name, None)
        else:
            return data.get(name, None)


class MediaField(forms.FileField):
    # widget = MediaInput
    default_error_messages = {
        'invalid_image': "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
    }

    def __init__(self, *args, **kwargs):

        required = kwargs.get('required', False)
        #widget = kwargs.pop('widget', None)
        # widget = MediaInput( attrs={
        #     'class': 'fields_bundle-media_field',
        #     # 'data-fields_bundle-media_field': self.image_field,
        #     # 'style': 'display:none;',
        # })
        # kwargs['widget'] = widget
        kwargs['label'] = ""

        super(MediaField, self).__init__(*args, **kwargs)


    def to_python(self, data):
        #print 'TO PYTHON DATA', data
        return data

    def has_changed(self, initial, data):
        #print 'CHANGED DATA', data, initial
        if data is None:
            return super(MediaField, self).has_changed(initial, data)
        return True

    def bound_data(self, data, initial):
        #print 'BOUND DATA', data, initial
        # if data in (None, FILE_INPUT_CONTRADICTION):
        #     return initial
        return data

    def clean(self, data, initial=None):
        if data is False:
            if not self.required:
                return False
            data = None
        if not data and initial:
            return initial
        return super(MediaField, self).clean(data)