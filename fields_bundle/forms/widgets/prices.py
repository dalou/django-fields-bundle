# encoding: utf-8
import re
import os
import logging
import locale
import json

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.forms.util import flatatt

from libs.utils.prices import price_format_currency_to_decimal, price_format_decimal_to_currency, DEFAULT_CURRENCY

class PriceWidget(forms.widgets.TextInput):

    class Media:
        # css = {
        #     'all': ('pretty.css',)
        # }
        js = (settings.STATIC_URL + 'cargo/forms/prices.js', )

    currency = DEFAULT_CURRENCY

    def __init__(self, *args, **kwargs):
        if 'currency' in kwargs:
            self.currency = kwargs['currency']
            del kwargs['currency']
        super(PriceWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        value = price_format_decimal_to_currency(value, self.currency)
        return super(PriceWidget, self).render(name, value, attrs)

    # def _has_changed(self, initial, data):
    #     return super(PriceWidget, self)._has_changed(self._format_value(initial), data)

class PriceInput(PriceWidget):
    pass