# encoding: utf-8

import time
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES

from localflavor.generic.forms import DateField, DateTimeField

from ..widgets.date import DateTimeInput, DatePickerInput, DateTimePickerInput

logger = logging.getLogger(__name__)


class FRDateField(DateField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DatePickerInput(
                format="%d/%m/%Y",
                attrs={'placeholder': 'jj/mm/aaaa', 'data-date-input': '{}'})
        super(FRDateField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # do not bother with parsing if the value is empty
        # and is authorized to be empty
        if not self.required and value in EMPTY_VALUES:
            return super(FRDateField, self).to_python(value)

        try:
            time.strptime(value,"%d/%m/%Y")
        except Exception, e:
            logger.exception(e)
            value = None
        return super(FRDateField, self).to_python(value)


class FRDateTimeField(DateTimeField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DateTimePickerInput(
                format="%d/%m/%Y %H:%M:%S",
                include_seconds=True,
                attrs={'placeholder': 'jj/mm/aaaa H:m:s', 'data-datetime-input': '{}'})
        super(FRDateTimeField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        try:
            time.strptime(value,"%d/%m/%Y %H:%M:%S")
        except Exception, e:
            value = None
        return super(FRDateTimeField, self).to_python(value)


class DateTimeField(DateField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = DateTimeInput(
                format="%m/%d/%Y %H:%M",
                attrs={'placeholder': 'jj/mm/aaaa'})
            kwargs['input_formats'] = ['%m/%d/%Y %H:%M']
        super(DateTimeField, self).__init__(*args, **kwargs)
