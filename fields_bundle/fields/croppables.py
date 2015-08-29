# from cStringIO import StringIO
# import os

# from django import forms
# from django.db.models import ImageField
# from django.db.models.fields.files import ImageFieldFile
# from django.core.files.base import ContentFile
# #from croppable.settings import IMAGE_FIELD_DELIMITER
# from libs.forms.widgets.croppables import CroppableImageWidget
# from libs.forms.fields.croppables import CroppableImageField as  CroppableImageFormField
# from io import BytesIO
# from PIL import Image
# IMAGE_FIELD_DELIMITER = "?"

# class CroppedImageFieldFile(ImageFieldFile):

#     coords = ''

#     def __init__(self, instance, field, name, coords):
#         self.coords = coords
#         super(ImageFieldFile, self).__init__( instance, field, name)

#         name = IMAGE_FIELD_DELIMITER.join([self.name, "cropped"])
#         #print self.storage.exists(name), name
#         if self.storage.exists(name):
#             self.name = name

#     def _get_url(self):
#         self._require_file()
#         #print self.storage.url(self.name)
#         return self.storage.url(self.name)
#     url = property(_get_url)

# class CroppableImageFieldFile(ImageFieldFile):

#     coords = ''
#     old_coords = ''
#     cropped = None
#     stashed_name = None

#     def __init__(self, instance, field, name):

#         if not hasattr(instance, field.name + '_stashed_name'):
#             setattr(instance, field.name + '_stashed_name', name)
#         self.stashed_name = getattr(instance, field.name + '_stashed_name')


#         super(ImageFieldFile, self).__init__( instance, field, name)

#         print instance, field, name

#         if name:

#             image_coords = name.split(IMAGE_FIELD_DELIMITER)
#             self.old_coords = self.stashed_name.split(IMAGE_FIELD_DELIMITER)[-1]

#             if len(image_coords) == 1:
#                 # image with no coords
#                 self.coords = ''
#                 self.filename = image_coords[0]
#                 self.name = self.filename

#             else:
#                 if image_coords[0].strip() == '':
#                     # update coords
#                     self.filename = self.stashed_name.split(IMAGE_FIELD_DELIMITER)[0]
#                     self.name = self.filename
#                     self.coords = image_coords[1]

#                 else:
#                     # update image and coords
#                     self.filename = image_coords[0]
#                     self.name = self.filename
#                     self.coords = image_coords[1]

#             self.cropped = CroppedImageFieldFile(instance, field, self.name, self.coords)

#         else:
#             self.old_coords = ''
#             self.filename = name

#     def save(self, name, content, save=True):

#          # If data_list[0] = image_file_field == None, form Field return coords alone
#         # old_coords = self.stashed_name.split(IMAGE_FIELD_DELIMITER)[-1]

#         manual = hasattr(self, 'old_coords') and hasattr(self, 'coords')

#         # if manual:
#         if self.old_coords != self.coords or not self._committed:

#             # new filename
#             self.filename = self.field.generate_filename(self.instance, self.filename)
#             old_filepath = self.stashed_name.split(IMAGE_FIELD_DELIMITER)[0]

#             #     # Original image has changed
#             if not self._committed:

#                 # reset old coords
#                 super(CroppableImageFieldFile, self).save(self.filename, content, save=False)
#                 self.filename = getattr(self.instance, self.field.name).name

#             else:
#                 try:
#                     content = self.storage.open(old_filepath)
#                     super(CroppableImageFieldFile, self).save(self.filename, content, save=False)
#                 except:
#                     pass
#                 self.filename = getattr(self.instance, self.field.name).name


#             #file_name, file_ext = os.path.splitext(old_filepath)
#             old_filepath = self.stashed_name.split(IMAGE_FIELD_DELIMITER)[0]
#             old_filepath_cropped = IMAGE_FIELD_DELIMITER.join([old_filepath, "cropped"]) #"%s_cropped%s" % (file_name, file_ext)



#             filename_cropped = IMAGE_FIELD_DELIMITER.join([self.filename, "cropped"])
#             file_name, file_ext = os.path.splitext(self.filename)
#             if file_ext in ['.jpg', '.jpeg']:
#                 FTYPE = 'JPEG'
#             elif file_ext == '.gif':
#                 FTYPE = 'GIF'
#             elif file_ext == '.png':
#                 FTYPE = 'PNG'
#             else:
#                 FTYPE = 'PNG'

#             coords = self.coords.split('_')
#             if len(coords) == 4:
#                 x, y, w, h = map(int, coords)
#                 original_im = Image.open(self.storage.open(self.filename, 'r'))
#                 cropped_im_tmp = StringIO()
#                 cropped_im = original_im.crop((x, y, x+w, y+h))
#                 cropped_im.save(cropped_im_tmp, FTYPE)
#                 cropped_im_tmp.seek(0)

#                 self.storage.save(filename_cropped, ContentFile(cropped_im_tmp.read()))
#                 cropped_im_tmp.close()

#             try:
#                 self.storage.delete(old_filepath)
#             except Exception, e:
#                 pass
#                 # print e.message
#             try:
#                 self.storage.delete(old_filepath_cropped)
#             except Exception, e:
#                 pass
#                 # print e.message

#         self.name = IMAGE_FIELD_DELIMITER.join([self.filename, self.coords])
#         setattr(self.instance, self.field.name, self.name)

#         if save:
#             self.instance.save()


# class CroppableImageField(ImageField):
#     #attr_class = CroppableImageFieldFile
#     attr_class = CroppableImageFieldFile


#     def __init__(self, *args, **kwargs):

#         super(CroppableImageField, self).__init__(*args, **kwargs)

#     def to_python(self, data):
#         """
#         Checks that the file-upload field data contains a valid image (GIF, JPG,
#         PNG, possibly others -- whatever the Python Imaging Library supports).
#         """
#         try:
#             f = super(CroppableImageField, self).to_python(data)
#             if f is None:
#                 return None
#         except:
#             return None

#         from django.utils.image import Image

#         # We need to get a file object for Pillow. We might have a path or we might
#         # have to read the data into memory.
#         if hasattr(data, 'temporary_file_path'):
#             file = data.temporary_file_path()
#         else:
#             if hasattr(data, 'read'):
#                 file = BytesIO(data.read())
#             elif isinstance(data, dict):
#                 file = BytesIO(data['content'])
#             else:
#                 return None

#         try:
#             # load() could spot a truncated JPEG, but it loads the entire
#             # image in memory, which is a DoS vector. See #3848 and #18520.
#             # verify() must be called immediately after the constructor.
#             Image.open(file).verify()
#         except Exception:
#             # Pillow (or PIL) doesn't recognize it as an image.
#             six.reraise(ValidationError, ValidationError(
#                 self.error_messages['invalid_image'],
#                 code='invalid_image',
#             ), sys.exc_info()[2])
#         if hasattr(f, 'seek') and callable(f.seek):
#             f.seek(0)
#         return f

#     # override this to allow saves even if the image file doesn't change (to update crop coordinates)
#     def pre_save(self, model_instance, add):
#         file = getattr(model_instance, self.attname)
#         if file:
#             file.save(file.name, file, save=False)
#         return file


#     def formfield(self, **kwargs):
#         defaults = {
#             'form_class': CroppableImageFormField,
#             'widget' : CroppableImageWidget(attrs={
#                 'class': 'image-ratio',
#             })
#         }
#         defaults.update(kwargs)
#         return super(CroppableImageField, self).formfield(**defaults)
