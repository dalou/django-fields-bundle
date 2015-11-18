# encoding: utf-8

import re, os
from PIL import Image
from cStringIO import StringIO
from io import BytesIO
from inspect import getargspec

from django import forms
from django.db.models import TextField, FileField
from django.core.files.base import File
from django.utils import six
from django.db.models.fields.files import ImageFieldFile, ImageFile, FieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from fields_bundle.forms import MediaField as MediaFormField, MediaInput
from fields_bundle.forms.media import EMBED_TYPES

IMAGE_FIELD_DELIMITER = "?"

# - Youtube
# - Soundcloud
# - Vimeo
# - Bandcamp
# - Pinterest
# - Mixcloud
# - Dailymotion



class MediaFieldImage(FieldFile):
    type = 'image'
    is_image = True

    def _get_html(self):
        if self.name and not self.type in self.field.authorized_types:
            return ''
        return """<img class="fields_bundle-media" src="%s" />""" % self.url
    html = property(_get_html)

    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, name)

        # print 'MediaFieldImage.save', name

        args, varargs, varkw, defaults = getargspec(self.storage.save)
        if 'max_length' in args:
            self.name = self.storage.save(name, content, max_length=self.field.max_length)
        else:
            warnings.warn(
                'Backwards compatibility for storage backends without '
                'support for the `max_length` argument in '
                'Storage.save() will be removed in Django 1.10.',
                RemovedInDjango110Warning, stacklevel=2
            )
            self.name = self.storage.save(name, content)

        # setattr(self.instance, self.field.name, self.name)

        # Update the filesize cache
        self._size = content.size
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()
        return self
    save.alters_data = True



# Can be File
class MediaFieldEmbed(object):
    is_embed = True
    _committed = False

    def __init__(self, instance, field, name, type="youtube"):
        self.name = name
        self.field = field
        self.instance = instance
        self.type = type

    def save(self, name, value, save=True):

        for type_name, patterns in EMBED_TYPES.items():
            for pattern in patterns:
                # regex = re.compile(pattern)
                result = re.search(pattern[0], name)
                if result:
                    print 'SAVE WITH RESULT', result.group(0)
                    self.type = type_name
                    self.name = result.group(0)

        setattr(self.instance, self.field.name, self.name)
        return self


    def _get_html(self):
        if self.name and not self.type in self.field.authorized_types:
            return ''


        patterns = EMBED_TYPES.get(self.type)
        if patterns:
            for pattern in patterns:
                result = re.search(pattern[0], self.name)
                html = re.sub(pattern[0], pattern[1], self.name)
                if html != self.name:
                    return html
        return ''
    html = property(_get_html)

    # def __init__(self, instance, field, name):

    #     if not hasattr(instance, field.name + '_stashed_name'):
    #         setattr(instance, field.name + '_stashed_name', name)
    #     self.stashed_name = getattr(instance, field.name + '_stashed_name')


    #     super(FieldFile, self).__init__(None, name)
    #     self.instance = instance
    #     self.field = field
    #     self.storage = field.storage
    #     self._committed = True


    #     print 'MediaFieldValue.__init__ : stashed_name : ', self.stashed_name, type( self.stashed_name)

    #     if self.stashed_name and self.stashed_name.strip != "" and len(self.stashed_name.split('|')) >= 2:

    #         self.stashed_type = self.stashed_name.split('|')[0] if self.stashed_name else None
    #         self.stashed_name = self.stashed_name.split('|')[1] if self.stashed_name else None
    #     else:
    #         self.stashed_type = None
    #         self.stashed_name = None

    #     print 'MediaFieldValue.__init__ : name : ', name, type(name)


    #     self.type = name.split('|')[0] if name else None
    #     self.name = name.split('|')[1]  if name else None

    #     print
    #     print "MediaFieldValue.__init__ : MEDIA FIELD:", self.type, self.name
    #     print "MediaFieldValue.__init__ : STASHED:", self.stashed_type, self.stashed_name
    #     print


    # def is_file(self):
    #     return self.type in ['image']

    # def is_image(self, stashed=False):
    #     return (self.type if not stashed else self.stashed_type) in ['image']

    # def _get_url(self):
    #     if self.is_file():
    #         return super(MediaFieldValue, self)._get_url()
    #     return None

    # def _get_path(self):
    #     if self.is_file():
    #         return super(MediaFieldValue, self)._get_path()
    #     return None

    # def _get_html(self):
    #     if not self.type in self.field.authorized_types:
    #         return None

    #     if self.is_image():
    #         return """<img class="fields_bundle-media" src="%s" />""" % self.name
    #     elif self.type in ['youtube']:
    #         return """<iframe class="fields_bundle-media" src="%s" frameborder="0" allowfullscreen></iframe>""" % self.name
    #     elif self.type in ['soundcloud']:
    #         return """<iframe class="fields_bundle-media" src="%s" scrolling="no" frameborder="0" allowfullscreen></iframe>""" % self.name
    #     else:
    #         return """<iframe class="fields_bundle-media" src="%s" scrolling="no" frameborder="0" allowfullscreen></iframe>""" % self.name
    # html = property(_get_html)

    # def save(self, name, content, save=True):


    #     type = None

    #     # Delete previous saved storage content if exists
    #     if self.is_image(stashed=True) and not self._committed:
    #         self.storage.delete(self.stashed_name)

    #     # If image
    #     if not self._committed:
    #         name = self.field.generate_filename(self.instance, name)
    #         args, varargs, varkw, defaults = getargspec(self.storage.save)

    #         if 'max_length' in args:
    #             self.name = self.storage.save(name, content, max_length=self.field.max_length)
    #         else:
    #             self.name = self.storage.save(name, content)
    #         type = "image"

    #         setattr(self.instance, self.field.name, name)
    #         self.name = name

    #         # Update the filesize cache
    #         self._size = content.size
    #         self._committed = True

    #         # Save the object because it has changed, unless save is False
    #         if save:
    #             self.instance.save()

    #     if type and name and type in self.field.authorized_types:

    #         combined = "%s|%s" % (type, name)
    #         setattr(self.instance, self.field.name, )
    #         self._committed = True
    #         return combined

    #     else:
    #         return None

    # save.alters_data = True

    # def delete(self, save=True):
    #     # Clear the image dimensions cache
    #     if hasattr(self, '_dimensions_cache'):
    #         del self._dimensions_cache
    #     super(MediaFieldValue, self).delete(save)





class MediaDescriptor(object):
    """
    The descriptor for the file attribute on the model instance. Returns a
    FieldFile when accessed so you can do stuff like::

        >>> from myapp.models import MyModel
        >>> instance = MyModel.objects.get(pk=1)
        >>> instance.file.size

    Assigns a file object on assignment so you can do::

        >>> with open('/tmp/hello.world', 'r') as f:
        ...     instance.file = File(f)

    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))


        value = instance.__dict__[self.field.name]

        #print
        #print 'MediaDescriptor.__get__ : IN : ', self.field.name, value, type(value)

        if value in [None, False, '']:
            value = None

        # Si on recupere la valeur unicode c'est la valeur en DB il faut la decompiler et
        # dispatcher vers le bon attr_class
        elif isinstance(value, six.string_types):

            type_value = value.split('|')
            if len(type_value) < 2:
                value_type = 'image'
                value = MediaFieldEmbed(instance, self.field, type_value[0])
            else:
                value_type = type_value[0]
                if value_type in ['image']:
                    value = MediaFieldImage(instance, self.field, type_value[1])
                else:
                    value = MediaFieldEmbed(instance, self.field, type_value[1], type=value_type)


            # value = 'image|%s' % name
            # attr = self.field.attr_class(instance, self.field, value)
            # instance.__dict__[self.field.name] = attr

        # Other types of files may be assigned as well, but they need to have
        # the FieldFile interface added to them. Thus, we wrap any other type of
        # File inside a FieldFile (well, the field's attr_class, which is
        # usually FieldFile).
        elif (isinstance(value, File)) and \
            not isinstance(value, MediaFieldImage):
            value = MediaFieldImage(instance, self.field, value.name)
            value.file = instance.__dict__[self.field.name]
            value._committed = False

        # Finally, because of the (some would say boneheaded) way pickle works,
        # the underlying FieldFile might not actually itself have an associated
        # file. So we need to reset the details of the FieldFile in those cases.
        elif isinstance(value, MediaFieldImage): # and not hasattr(value, 'field'):
            value.instance = instance
            value.field = self.field
            value.storage = self.field.storage
            # print "Already an image", value.name

        # Finally, because of the (some would say boneheaded) way pickle works,
        # the underlying FieldFile might not actually itself have an associated
        # file. So we need to reset the details of the FieldFile in those cases.
        elif isinstance(value, MediaFieldEmbed): # and not hasattr(value, 'field'):
            value.instance = instance
            value.field = self.field

        else:
            value = None

        instance.__dict__[self.field.name] = value

        # That was fun, wasn't it?
        # print 'MediaDescriptor.__get__ : OUT : ', self.field.name, value, type(value)
        #print
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value
        # print 'MediaDescriptor.__set__ : ', self.field.name, value, type(value)
        # previous_file = instance.__dict__.get(self.field.name)
        # print 'previous_file', previous_file

        # if previous_file is not None:
        #     self.field.update_dimension_fields(instance, force=True)




class MediaField(FileField):
    descriptor_class = MediaDescriptor

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


    def to_python(self, value):
        """
        Converts the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. Subclasses should override this.
        """
        # print "MediaField.to_python : ", value, type(value)
        return value

    def save_form_data(self, instance, data):
        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        if data is not None:
            # This value will be converted to unicode and stored in the
            # database, so leaving False as-is is not acceptable.
            if not data:
                data = ''
            setattr(instance, self.name, data)

    # override this to allow saves even if the image file doesn't change (to update crop coordinates)
    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        value = getattr(model_instance, self.attname)
        if value and not value._committed:
        #     # Commit the file to storage prior to saving the model

            value = value.save(value.name, value, save=False)
        if value is not None:
            value = "%s|%s" % (value.type, value.name)
        else:
            value = None
        # print
        # print "MediaField.pre_save : ", self.name, value, type(value)
        # print
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

