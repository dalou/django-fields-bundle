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

from sorl.thumbnail.shortcuts import get_thumbnail
from floppyforms import ClearableFileInput

logger = logging.getLogger(__name__)




class ImageThumbnailFileInput(ClearableFileInput):
    template_name = 'forms/widgets/_image_input.html'








class FileInput(OriginalFileInput):
    """
    Widget prodiving a input element for file uploads based on the
    Django ``FileInput`` element. It hides the actual browser-specific
    input element and shows the available image for images that have
    been previously uploaded. Selecting the image will open the file
    dialog and allow for selecting a new or replacing image file.
    """
    template_name = 'form/widget/file_input.html'
    attrs = {'accept': 'file/*'}

    original_filename = None

    def render(self, name, value, attrs=None):
        """
        Render the ``input`` field based on the defined ``template_name``. The
        image URL is take from *value* and is provided to the template as
        ``image_url`` context variable relative to ``MEDIA_URL``. Further
        attributes for the ``input`` element are provide in ``input_attrs`` and
        contain parameters specified in *attrs* and *name*.
        If *value* contains no valid image URL an empty string will be provided
        in the context.
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        file_url = final_attrs.get('value', '')
        file_original_url = None
        file_name = self.original_filename
        if not file_name and file_url:
            file_original_url = os.path.join(settings.MEDIA_URL, file_url)
            file_name = os.path.basename(file_url)

        return render_to_string(self.template_name, Context({
            'input_attrs': flatatt(final_attrs),
            'file_url': file_url,
            'file_name': file_name,
            'file_original_url': file_original_url,
            'file_id': "%s-file" % final_attrs['id'],
        }))

