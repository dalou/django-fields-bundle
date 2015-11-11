# encoding: utf-8

import re, os
from PIL import Image
from cStringIO import StringIO
from io import BytesIO
from inspect import getargspec

from django import forms
from django.db.models import FileField
from django.db.models.fields.files import ImageFieldFile, ImageFile, FieldFile
from django.core.files.base import ContentFile

from fields_bundle.forms import MediaField as MediaFormField, MediaInput

IMAGE_FIELD_DELIMITER = "?"

# - Youtube
# - Soundcloud
# - Vimeo
# - Bandcamp
# - Pinterest
# - Mixcloud
# - Dailymotion

# Can be File
class MediaFieldValue(FieldFile):

    def __init__(self, instance, field, name):

        if not hasattr(instance, field.name + '_stashed_name'):
            setattr(instance, field.name + '_stashed_name', name)
        self.stashed_name = getattr(instance, field.name + '_stashed_name')

        super(FieldFile, self).__init__(None, name)
        self.instance = instance
        self.field = field
        self.storage = field.storage
        self._committed = True

    def get_type_name(self, last_value=False):
        if last_value:
            return self.stashed_name.partition('|')[::2] if self.stashed_name else (None, None)
        else:
            return self.name.partition('|')[::2] if self.name else (None, None)

    def is_image(self):
        media_type, name = self.get_type_name()
        return media_type in ['image']

    def _get_url(self):
        if self.is_image():
            media_type, name = self.get_type_name()
            return self.storage.url(name)
        return None

    def _get_html(self):
        media_type, name = self.get_type_name()
        if not media_type in self.field.authorized_types:
            return None

        if media_type in ['image']:
            self._require_file()
            return """<img class="fields_bundle-media" src="%s" />""" % self.storage.url(name)
        elif media_type in ['youtube']:
            return """<iframe class="fields_bundle-media" src="%s" frameborder="0" allowfullscreen></iframe>""" % name
        elif media_type in ['soundcloud']:
            return """<iframe class="fields_bundle-media" src="%s" scrolling="no" frameborder="0" allowfullscreen></iframe>""" % name
        else:
            return """<iframe class="fields_bundle-media" src="%s" scrolling="no" frameborder="0" allowfullscreen></iframe>""" % name
    html = property(_get_html)

    def save(self, name, content, save=True):

        print name, type(name)
        print content, type(content)

        final_name = None

        # Delete previous saved storage content if exists
        old_media_type, old_name = self.get_type_name(last_value=True)
        if old_name and not self._committed:
            self.storage.delete(old_name)


        youtube = re.search(r'(http[s]?\:\/\/www\.youtube\.com\/embed\/[^"]+)"?', name)
        if youtube:
            self.name = final_name = "youtube|%s" % youtube.group(1)
            setattr(self.instance, self.field.name, name)
            self._committed = True

        soundcloud = re.search(r'(http[s]?\:\/\/[w]+\.soundcloud\.com\/player\/[^"]+)"?', name)
        if soundcloud:
            self.name = final_name = "soundcloud|%s" % soundcloud.group(1)
            setattr(self.instance, self.field.name, name)

        if final_name:
            media_type, name = self.get_type_name()
            if not media_type in self.field.authorized_types:
                return None
            else:
                self._committed = True

        # If image
        if not final_name and not self._committed:
            name = self.field.generate_filename(self.instance, name)
            args, varargs, varkw, defaults = getargspec(self.storage.save)

            if 'max_length' in args:
                self.name = self.storage.save(name, content, max_length=self.field.max_length)
            else:
                self.name = self.storage.save(name, content)
            final_name = "image|%s" % name

            setattr(self.instance, self.field.name, final_name)
            self.name = final_name

            # Update the filesize cache
            self._size = content.size
            self._committed = True

            # Save the object because it has changed, unless save is False
            if save:
                self.instance.save()
            return self


        else:
            return self
    save.alters_data = True

    def delete(self, save=True):
        # Clear the image dimensions cache
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super(MediaFieldValue, self).delete(save)










class MediaField(FileField):
    attr_class = MediaFieldValue

    def __init__(self, *args, **kwargs):
        # if kwargs.get('image_field'):
        #     self.image_field = kwargs.pop('image_field')



        self.crop_image = True
        if kwargs.get('crop_image'):
            self.crop_image = kwargs.pop('crop_image')

        self.authorized_types = ['image', 'youtube', 'dailymotion']
        if kwargs.get('authorized_types'):
            self.authorized_types = kwargs.pop('authorized_types')

        kwargs['max_length'] = 255

        super(MediaField, self).__init__(*args, **kwargs)
        self.old_name = self.name



    # override this to allow saves even if the image file doesn't change (to update crop coordinates)
    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        value = file = getattr(model_instance, self.attname)
        if file:
            # Commit the file to storage prior to saving the model
            value = file.save(file.name, file, save=False)
        return value



    def formfield(self, **kwargs):
        defaults = {
        }
        defaults.update(kwargs)
        defaults['form_class'] = MediaFormField
        defaults['widget'] = MediaInput(
            attrs = { 'class': 'image-ratio', },
            authorized_types = self.authorized_types,
        )
        return super(MediaField, self).formfield(**defaults)

