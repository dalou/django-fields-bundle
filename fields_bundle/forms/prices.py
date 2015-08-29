# encoding: utf-8
import re
import os
import logging
import locale
import json

from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.forms.util import flatatt


from babel.numbers import format_number, format_decimal, format_percent


DEFAULT_CURRENCY = 'EUR'
# Send in data way to assets/js/input_format.js
CURRENCY_PATTERNS = {
    'EUR': { 'format': u'%s €', 'locale': 'fr_FR', 'spacing': ' ', 'decimal': ',', 'placeholder': 'EUR' },
    'USD': { 'format': u'$%s', 'locale': 'en_US', 'spacing': ',', 'decimal': '.', 'placeholder': 'USD' },
}

def price_format_decimal_to_currency(value, currency='EUR'):
    if value:
        try:
            if currency in CURRENCY_PATTERNS.keys():
                value = CURRENCY_PATTERNS[currency]['format'] % format_number(value, locale = CURRENCY_PATTERNS[currency]['locale'])
            else:
                return value
        except:
            return value
    return value

def price_format_currency_to_decimal(value, currency='EUR'):
    if value == None:
        return None
    value = unicode(value)
    if value.strip() == '':
        return None

    float_value = ""
    float_lock = False
    for c in value[::-1]:
        if c.isdigit():
            float_value += c
        if not float_lock and (c == '.' or c == ','):
            float_value += '.'
            float_lock = True

    try:
        return float(float_value[::-1]);
    except:
        return None


# In relation to assets/js/input_format.js
class PriceField(forms.IntegerField):

    currency = DEFAULT_CURRENCY

    def __init__(self, *args, **kwargs):
        self.currency = kwargs['currency'] if 'currency' in kwargs else self.currency
        if 'widget' not in kwargs:
            kwargs['widget'] = PriceWidget(
                currency=self.currency,
                attrs={
                    'placeholder': self.currency,
                    'class': 'price-formated',
                    'data-currency': self.currency,
                    'data-currency-patterns': original_json.dumps(CURRENCY_PATTERNS)
                })
            del kwargs['currency']
        super(PriceField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': _(u'Cette valeur doit être décimale.'),
    }
    def to_python(self, value):
        # if not value.isdigit():
        #     raise ValidationError(self.error_messages['invalid'])
        return price_format_currency_to_decimal(value, self.currency)


class PriceWidget(forms.widgets.TextInput):

    class Media:
        # css = {
        #     'all': ('pretty.css',)
        # }
        js = (settings.STATIC_URL + 'fields_bundle/prices.js', )

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