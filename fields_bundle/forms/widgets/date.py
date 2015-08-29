import re
import os
import logging
from libs import original_json as json

from django.conf import settings
from django import forms
from django.template import Context
from django.forms.widgets import FileInput as OriginalFileInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from sorl.thumbnail.shortcuts import get_thumbnail

logger = logging.getLogger(__name__)


# class DatePickerInput(forms.DateInput):
#     """
#     DatePicker input that uses the jQuery UI datepicker.  Data attributes are
#     used to pass the date format to the JS
#     """
#     def __init__(self, *args, **kwargs):
#         super(DatePickerInput, self).__init__(*args, **kwargs)
#         add_js_formats(self)

class DateInput(forms.DateTimeInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.

    class Media:
        css = {
            'all': (settings.STATIC_URL + 'vendors/jquery.datepicker.css',)
        }
        js = (settings.STATIC_URL + 'vendors/jquery.datetimepicker.js',)

    input_type = 'date'

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)

        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': False,
            'mask': True,
            'format': 'd/m/Y H:i'
            #'format': 'd.m.Y'
        })
        super(DateInput, self).__init__(*args, **kwargs)

        # if not include_seconds:
        #     self.format = re.sub(':?%S', '', self.format)
        attrs = {
            'data-date-input': json.dumps(options)
        }
        self.attrs.update(attrs)

    def render_script(self, id):
        return '''<script type="text/javascript">

                    $('#%(id)s').on('mousedown', function() {
                        if(!this.datetimepicker) {
                            $(this).datetimepicker($(this).data('datetime-input'));
                            this.datetimepicker = true;
                        }
                    });
                </script>
                ''' % { 'id' : id }


    def render(self, name, value, attrs={}):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        render = super(DateInput, self).render(name, value, attrs)
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'])))

class DateTimeInput(DateInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.
    input_type = 'datetime'

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)

        options = kwargs.pop('options', {
            'lang': 'fr',
            'timepicker': True,
            'mask': True,
            'format': 'd/m/Y H:i'
            #'format': 'd.m.Y'
        })
        super(DateTimeInput, self).__init__(*args, **kwargs)

        # if not include_seconds:
        #     self.format = re.sub(':?%S', '', self.format)

        attrs = {
            'data-datetime-input': json.dumps(options)
        }
        self.attrs.update(attrs)


def datetime_format_to_js_date_format(format):
    """
    Convert a Python datetime format to a date format suitable for use with JS
    date pickers
    """
    converted = format
    replacements = {
        '%Y': 'yy',
        '%m': 'mm',
        '%d': 'dd',
        '%H:%M': '',
    }
    for search, replace in replacements.iteritems():
        converted = converted.replace(search, replace)
    return converted.strip()


def datetime_format_to_js_time_format(format):
    """
    Convert a Python datetime format to a time format suitable for use with JS
    date pickers
    """
    converted = format
    replacements = {
        '%Y': '',
        '%m': '',
        '%d': '',
        '%H': 'HH',
        '%M': 'mm',
    }
    for search, replace in replacements.iteritems():
        converted = converted.replace(search, replace)

    converted = re.sub('[-/][^%]', '', converted)

    return converted.strip()


def add_js_formats(widget, options):
    """
    Set data attributes for date and time format on a widget
    """
    attrs = {
        'data-datetime-input': json.dumps(options)
    }
    widget.attrs.update(attrs)







# ALL BOTTOM CONTENT ARE DEPRECATED
def old_add_js_formats(widget):
    """
    Set data attributes for date and time format on a widget
    """
    attrs = {
        'data-dateFormat': datetime_format_to_js_date_format(
            widget.format),
        'data-timeFormat': datetime_format_to_js_time_format(
            widget.format)
    }
    widget.attrs.update(attrs)


class DatePickerInput(forms.DateInput):
    """
    DatePicker input that uses the jQuery UI datepicker.  Data attributes are
    used to pass the date format to the JS
    """
    def __init__(self, *args, **kwargs):
        super(DatePickerInput, self).__init__(*args, **kwargs)
        old_add_js_formats(self)


class DateTimePickerInput(forms.DateTimeInput):
    # Build a widget which uses the locale datetime format but without seconds.
    # We also use data attributes to pass these formats to the JS datepicker.

    def __init__(self, *args, **kwargs):
        include_seconds = kwargs.pop('include_seconds', False)
        super(DateTimePickerInput, self).__init__(*args, **kwargs)

        if not include_seconds:
            self.format = re.sub(':?%S', '', self.format)
        old_add_js_formats(self)
