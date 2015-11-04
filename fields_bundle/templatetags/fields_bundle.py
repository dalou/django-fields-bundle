# encoding: utf-8

import datetime

from django import template
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from taggit_templatetags.templatetags.taggit_extras import get_queryset

register = template.Library()


@register.inclusion_tag('fields_bundle/_tinymce_inline.html')
def fields_bundle_tinymce_inline(field, config='default', default=None):
    return {
        'field': field,
        'config': config,
        'default': default,
    }

@register.inclusion_tag('fields_bundle/_image_cropped_input.html')
def fields_bundle_image_cropped(image_field, image_cropped_field, empty_message="<span>+</span>"):
    return {
        'empty_message': empty_message,
        'image_field': image_field,
        'image_cropped_field': image_cropped_field,
    }