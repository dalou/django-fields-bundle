# encoding: utf-8
import re
import os
import logging
import locale
from libs import original_json

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.forms.util import flatatt

from libs.utils.prices import price_format_currency_to_decimal, price_format_decimal_to_currency, DEFAULT_CURRENCY, CURRENCY_PATTERNS
from libs.forms.widgets import PriceWidget

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