# import os

# from django import forms
# from django.forms.fields import ImageField
# #from croppable.settings import IMAGE_FIELD_DELIMITER
# from libs.forms.widgets.croppables import CroppableImageWidget
# from django.contrib.admin.widgets import AdminFileWidget
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.admin.widgets import AdminFileWidget
# from io import BytesIO

# from PIL import Image

# IMAGE_FIELD_DELIMITER = "?"

# class BaseCroppableImageField(ImageField):
#     default_error_messages = {
#         'invalid_image': _("Upload a valid image. The file you uploaded was either not an image or a corrupted image."),
#     }

#     def to_python(self, data):
#         """
#         Checks that the file-upload field data contains a valid image (GIF, JPG,
#         PNG, possibly others -- whatever the Python Imaging Library supports).
#         """
#         try:
#             f = super(BaseCroppableImageField, self).to_python(data)
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
#             else:
#                 file = BytesIO(data['content'])

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

# class CroppableImageField(forms.MultiValueField):#forms.ImageField):
#     widget = CroppableImageWidget
#     default_error_messages = {
#         'invalid_image': _("Upload a valid image. The file you uploaded was either not an image or a corrupted image."),
#     }

#     def __init__(self, *args, **kwargs):

#         required = kwargs.get('required', False)
#         widget = kwargs.pop('widget')

#         # print widget == AdminFileWidget, isinstance(widget, AdminFileWidget), widget
#         # print

#         if widget:
#             if widget == AdminFileWidget or isinstance(widget, AdminFileWidget):
#                 widget = CroppableImageWidget()
#             kwargs['widget'] = widget

#         # self.widget = widget
#         fields = (
#             BaseCroppableImageField(),
#             forms.CharField(),
#         )

#         kwargs.pop('max_length')

#         super(CroppableImageField, self).__init__(fields, *args, **kwargs)




#         # print isinstance(self.widget, AdminFileWidget), self.widget, self.required, args, kwargs
#         # print
#         self.widget.is_required = self.required

#         # print self.required, self.widget, self.widget.is_required

#     #  you need to implement compress() in a MultiValueField subclass to return a single value for the form's cleaned_data
#     def compress(self, data_list):
#         if data_list:

#             # Examples
#             # [None, '5_4_7_10'] => delete image
#             # ['', '5_4_7_10'] => update coords
#             # ['path/to/image', '5_4_7_10'] => update image & coords

#             # if the widget returns False as opposed to None, the "clear" checkbox was checked (this is a Django thing)
#             if data_list[0] is False:
#                 return False

#             image_file = data_list[0]
#             coords = data_list[1]

#             # an image won't exist here if the image field is being cleared by the user
#             if image_file:
#                 if IMAGE_FIELD_DELIMITER in image_file.name:
#                     raise forms.ValidationError('You cannot upload image files containing the image field delimiter: \"' + \
#                                                 IMAGE_FIELD_DELIMITER + '\".  You can configure this with the \
#                                                 IMAGE_FIELD_DELIMITER setting')

#                 image_file.name = IMAGE_FIELD_DELIMITER.join([image_file.name, coords])
#                 return image_file

#             return IMAGE_FIELD_DELIMITER.join(['', coords])

#         return None


# import copy, random
# from itertools import chain
# import warnings

# from django.conf import settings
# from django.forms.utils import flatatt, to_current_timezone
# from django.utils.datastructures import MultiValueDict, MergeDict
# from django.utils.encoding import force_text, python_2_unicode_compatible
# from django.utils.html import conditional_escape, format_html
# from django.utils.translation import ugettext_lazy
# from django.utils.safestring import mark_safe
# from django.utils import formats, six
# from django.utils.six.moves.urllib.parse import urljoin
# from django.forms.widgets import (
#     MultiWidget,
#     HiddenInput,
#     TextInput,
#     ClearableFileInput,
#     FileInput as OriginalFileInput,
#     CheckboxInput
# )

# class CroppableWidget(ClearableFileInput):

#     template_with_initial = u"""
#     <div class="cargo-image-croppable" data-image-croppable="%(croppable_options)s">
#         %(initial_text)s:
#         <div class="cargo-image-croppable-container" style="
#             max-height: 400px;
#         ">%(initial)s
#         </div>
#         %(clear_template)s<br />
#         %(input_text)s: %(input)s
#     </div>
#     """

#     template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

#     url_markup_template = u"""<img  src="{0}?rand=%s" style="width:100%%; max-height:400px;" />""" % random.randint(0,1000000)

#     class Media:


#         css = {
#             'all': (
#                 # settings.STATIC_URL + 'cargo/croppable/jquery.croppable.css',
#                 settings.STATIC_URL + 'vendors/cropper.css',
#             )
#         }
#         js = (
#             # settings.STATIC_URL + 'cargo/croppable/jquery.croppable.min.js',
#             settings.STATIC_URL + 'vendors/cropper.js',
#             settings.STATIC_URL + 'js/cropper.js',
#         )

#     def render(self, name, value, attrs=None):
#         substitutions = {
#             'initial_text': self.initial_text,
#             'input_text': self.input_text,
#             'clear_template': '',
#             'clear_checkbox_label': self.clear_checkbox_label,
#         }
#         template = """
#         <div class="cargo-image-croppable" data-image-croppable="%(croppable_options)s">
#             <div class="cargo-image-croppable-container"></div>
#             %(input)s
#         </div>
#         """
#         substitutions['croppable_options'] = {}
#         substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

#         # print value, self.is_required
#         if value and hasattr(value, "url"):
#             template = self.template_with_initial
#             substitutions['initial'] = format_html(self.url_markup_template,
#                                                    value.url,
#                                                    force_text(value))
#             if not self.is_required:
#                 checkbox_name = self.clear_checkbox_name(name)
#                 checkbox_id = self.clear_checkbox_id(checkbox_name)
#                 substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
#                 substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
#                 substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
#                 substitutions['clear_template'] = self.template_with_clear % substitutions

#         return mark_safe(template % substitutions)

#     # template = u"""
#     # <div id="%(name)s_croppable-image-field" class="croppable-image-field">
#     #     <div class="croppable-image-field-cropper col-sm-6" style="width:50%%; float:left;">
#     #         <h3>Image originale</h3>
#     #         <div id="%(name)s_croppable-image-field-cropper" style="background:black; width:100%%;">
#     #             <img class="croppable-image" src="%(initial)s" style="background:black; width:100%%;" />
#     #         </div>

#     #         %(input_text)s: %(input)s
#     #         <br />
#     #         %(clear_template)s
#     #         %(coords_template)s

#     #     </div>
#     #     <div class="croppable-image-field-initial-preview col-sm-6" style="width:50%%; float:left;">

#     #             <div class="croppable-image-field-initial">

#     #                 %(initial_img)s
#     #             </div>
#     #             <!--<div class="croppable-image-field-preview">
#     #                 <h3>Apercu</h3>
#     #                 <div class="cropper-viewer croppable-image-preview" >

#     #                 </div>
#     #             </div>-->
#     #     </div>

#     # </div>
#     # <script type="text/javascript">

#     #     $(document).ready(function() {

#     #         $(document).on('mouseover', '.croppable-image-field', function(e, self, $self, setPreview) {


#     #             var last_empty_form = $(this).attr('id').indexOf("__prefix__") > -1

#     #             //console.log(last_empty_form, this.CARGO_CROPPABLE_IMAGE, this.CARGO_CROPPABLE_IMAGE != null || this.CARGO_CROPPABLE_IMAGE == 'undefined')


#     #             if(last_empty_form || this.CARGO_CROPPABLE_IMAGE != null || this.CARGO_CROPPABLE_IMAGE == 'undefined') return;

#     #             self = this;
#     #             $self = $(self);
#     #             var $cropper_container = $self.find('.cropper-container');
#     #             var $image = $self.find('.croppable-image'),
#     #                 $imageInput = $self.find('input[type=file]');

#     #             var $infosInput = $self.next().next();
#     #             var coords = $infosInput.val().split('_');
#     #                 initial = null;
#     #             if( coords.length == 4 ) {
#     #                 initial = {
#     #                     x: coords[0],
#     #                     y: coords[1],
#     #                     w: coords[2],
#     #                     h: coords[3]
#     #                 };
#     #             }
#     #             if($.fn.croppable) {
#     #                 $image.croppable({
#     #                     data: initial,
#     #                     preview: ".croppable-image-preview",
#     #                     done: function(data, purcents) {
#     #                         var val = data.x+ '_'+ data.y +'_'+ data.w + '_'+ data.h
#     #                         $infosInput.val(val);
#     #                     },
#     #                     file_input: $imageInput,
#     #                     file_dropzone: $self
#     #                 });

#     #                 if(this.CARGO_CROPPABLE_IMAGE == null) {
#     #                     this.CARGO_CROPPABLE_IMAGE = true;
#     #                 };
#     #             }






#     #         });
#     #         $('.croppable-image-field').mouseover();

#     #     });





#     # </script>
#     # """
#     # template_with_clear = u"""
#     #     %(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>
#     # """
#     # template_with_coords = u"""
#     #     %(coords)s
#     # """

#     # url_markup_template = '{0}'

#     # def __init__(self, *args, **kwargs):
#     #     super(CroppableWidget, self).__init__(*args, **kwargs)

#     # def coords_checkbox_name(self, name):
#     #     """
#     #     Given the name of the file input, return the name of the clear checkbox
#     #     input.
#     #     """
#     #     return name + '-coords'

#     # def coords_checkbox_id(self, name):
#     #     """
#     #     Given the name of the clear checkbox input, return the HTML id for it.
#     #     """
#     #     return name + '_id'

#     # def render(self, name, value, attrs=None):

#     #     substitutions = {
#     #         'initial_text': self.initial_text,
#     #         'input_text': self.input_text,
#     #         'clear_template': '',
#     #         'clear_checkbox_label': self.clear_checkbox_label,
#     #         'name': name,
#     #         'input': super(OriginalFileInput, self).render(name, value, attrs),
#     #         'initial_img': ("""
#     #             <h3>Actuellement</h3>
#     #             <img class="" src="%s?rand=%s" style="width:100%%;"/>
#     #             <hr />
#     #         """ % (value.cropped.url, random.randint(0,1000000))) if (value and hasattr(value, "cropped") and hasattr(value.cropped, "url")) else ''
#     #     }
#     #     # template = '%(input)s'
#     #     # substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

#     #     # if value and hasattr(value, "url"):
#     #     template = self.template
#     #     substitutions['initial'] = value.url if (value and hasattr(value, "url")) else ''
#     #     #format_html(self.url_markup_template,
#     #                                            # value.url if value and hasattr(value, "url") else '',
#     #                                            # force_text(value))

#     #     coords_checkbox_name = self.coords_checkbox_name(name)
#     #     coords_checkbox_id = self.coords_checkbox_id(coords_checkbox_name)

#     #     substitutions['coords_checkbox_name'] = conditional_escape(coords_checkbox_name)
#     #     substitutions['coords_checkbox_id'] = conditional_escape(coords_checkbox_id)
#     #     substitutions['coords'] = ''#HiddenInput().render(coords_checkbox_name, False, attrs={'id': coords_checkbox_id})
#     #     substitutions['coords_template'] = ''#self.template_with_coords % substitutions

#     #     if not self.is_required:
#     #         checkbox_name = self.clear_checkbox_name(name)
#     #         checkbox_id = self.clear_checkbox_id(checkbox_name)

#     #         substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
#     #         substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
#     #         substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
#     #         substitutions['clear_template'] = self.template_with_clear % substitutions

#     #     return mark_safe(template % substitutions)

#     # def value_from_datadict(self, data, files, name):
#     #     return super(CroppableImageWidget, self).value_from_datadict(data, files, name)





# class CroppableImageWidget(MultiWidget):

#     def __init__(self, image_widget=CroppableWidget, infos_widget=HiddenInput, attrs=None):

#         if attrs is not None:
#             self.attrs = attrs.copy()
#         else:
#             self.attrs = {}

#         widgets = (
#             image_widget,
#             infos_widget
#         )
#         super(CroppableImageWidget, self).__init__(widgets, attrs)
#         self.widgets[0].is_required = self.is_required

#     def decompress(self, value):
#         if value:
#             return [value, value.coords]
#         return ['', value]

#     def render(self, name, value, attrs):
#         # attrs['data-croppable-image-infos-field-id'] = attrs['id'] + '_1'
#         return super(CroppableImageWidget, self).render(name, value, attrs)