# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.utils.text import capfirst

from fields_bundle.forms import PriceField as PriceFormField, PriceInput


class PriceField(models.DecimalField):
    """
    A text field made to accept hexadecimal color value (#FFFFFF)
    with a color picker widget.
    """
    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = kwargs.get('decimal_places', 2)
        kwargs['max_digits'] = kwargs.get('max_digits', 21)
        super(PriceField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = PriceFormField
        return super(PriceField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fields_bundle\.fields\.PriceField"])
except ImportError:
    pass