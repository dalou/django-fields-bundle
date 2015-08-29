import re
import os
import logging

from django.conf import settings
from django import forms
from django.template import Context
from django.forms.widgets import FileInput as OriginalFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt

try:
    from sorl.thumbnail.shortcuts import get_thumbnail
except:
    def get_thumbnail(image_url, *args, **kwargs):
        return image_url

logger = logging.getLogger(__name__)



class ImageInput(OriginalFileInput):
    template_name = 'fields_bundle/_image_input.html'

# class ImageInput(OriginalFileInput):
#     """
#     Widget prodiving a input element for file uploads based on the
#     Django ``FileInput`` element. It hides the actual browser-specific
#     input element and shows the available image for images that have
#     been previously uploaded. Selecting the image will open the file
#     dialog and allow for selecting a new or replacing image file.
#     """
#     template_name = 'fields_bundle/_image_input.html'
#     attrs = { 'accept': 'image/*' }

#     def render(self, name, value, attrs=None):
#         """
#         Render the ``input`` field based on the defined ``template_name``. The
#         image URL is take from *value* and is provided to the template as
#         ``image_url`` context variable relative to ``MEDIA_URL``. Further
#         attributes for the ``input`` element are provide in ``input_attrs`` and
#         contain parameters specified in *attrs* and *name*.
#         If *value* contains no valid image URL an empty string will be provided
#         in the context.
#         """
#         if value is None:
#             value = ''

#         final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
#         if value != '':
#             # Only add the 'value' attribute if a value is non-empty.
#             final_attrs['value'] = force_unicode(self._format_value(value))

#         image_url = final_attrs.get('value', '')
#         image_original_url = None
#         image_thumb = None
#         if image_url:
#             image_original_url = os.path.join(settings.MEDIA_URL, image_url)
#             try:
#                 image_thumb = get_thumbnail(image_url, 'x100', crop='center', upscale=True)
#             except IOError as inst:
#                 logger.error(inst)

#         return render_to_string(self.template_name, Context({
#             'image_thumb': image_thumb,
#             'input_attrs': flatatt(final_attrs),
#             'image_url': image_url,
#             'image_original_url': image_original_url,
#             'image_id': "%s-image" % final_attrs['id'],
#             'name': "%s" % final_attrs['name'],
#         }))


