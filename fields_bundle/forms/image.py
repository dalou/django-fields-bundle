# encoding: utf-8

import re
import os
import logging

from django.conf import settings
from django import forms
from django.template import Context
from django.forms.widgets import FileInput as OriginalFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.utils import flatatt

try:
    from sorl.thumbnail.shortcuts import get_thumbnail
except:
    def get_thumbnail(image_url, *args, **kwargs):
        return image_url

logger = logging.getLogger(__name__)



class ImageInput(OriginalFileInput):
    template_name = 'fields_bundle/_image_input.html'


class CroppedImageInput(forms.widgets.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'fields_bundle/image_cropped.css',
            )
        }
        js = (
            settings.STATIC_URL + 'fields_bundle/image_cropped.js',
            # settings.STATIC_URL + 'js/cropper.js',
        )

class CroppedImageField(forms.CharField):
    widget = CroppedImageInput
    default_error_messages = {
        'invalid_image': "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
    }
    image_field = None


    def __init__(self, *args, **kwargs):

        required = kwargs.get('required', False)
        widget = kwargs.pop('widget', None)
        self.image_field = kwargs.pop('label')

        # print widget == AdminFileWidget, isinstance(widget, AdminFileWidget), widget
        # print


        # if widget:
        # if widget == AdminFileWidget or isinstance(widget, AdminFileWidget):
        widget = CroppedImageInput( attrs={
            'class': 'image-croppable',
            'data-fields_bundle-croppedimage': self.image_field,
            'style': 'display:none;',
        })
        kwargs['widget'] = widget
        kwargs['label'] = ""

        super(CroppedImageField, self).__init__(*args, **kwargs)


    def to_python(self, data):
        return super(CroppedImageField, self).to_python(data)