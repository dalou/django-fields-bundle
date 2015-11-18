from __future__ import unicode_literals
import os
import copy
import uuid
import urlparse
from django.conf import settings
import fields_bundle.settings
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import strip_tags
from django.utils.html import escape
from django.template import Context
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string

try:
    from collections import OrderedDict as SortedDict
except ImportError:
    from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext as _
import json
try:
    from django.utils.encoding import smart_text as smart_unicode
except ImportError:
    try:
        from django.utils.encoding import smart_unicode
    except ImportError:
        from django.forms.util import smart_unicode

def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)


class HtmlField(forms.CharField):
    def __init__(self, *args, **kwargs):

        attrs = kwargs.get('attrs', {})
        if not attrs.get('placeholder'):
            attrs['placeholder'] = kwargs.get('label', '')

        kwargs['widget'] = HtmlInput(
            tinymce=kwargs.pop('tinymce', None),
            inline=kwargs.pop('inline', False),
            attrs=kwargs.get('attrs', attrs)
        )
        super(HtmlField, self).__init__(*args, **kwargs)


class HtmlInput(forms.Textarea):

    class Media:
        js = [
            fields_bundle.settings.FIELDS_BUNDLE_TINYMCE_URL,
            'fields_bundle/html_input.js',
        ]
        css = {
            'all': ('fields_bundle/html_input.css', )
        }

    def __init__(self, attrs=None, tinymce=None, inline=False):
        super(HtmlInput, self).__init__(attrs=attrs)
        tinymce = tinymce or {}
        self.tinymce = tinymce
        self.inline = inline


    # USE BLEACH FOR FUTURE
    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value and self.tinymce and self.tinymce.get('apply_format') == "text":
            value = strip_tags(value.replace('<br />', '\n').replace('<br/>', '\n'))
        return value


    def get_config_json(self, config):
        # Fix for js functions
        js_functions = {}
        for k in ('paste_preprocess', 'paste_postprocess'):
            if k in config:
               js_functions[k] = config[k]
               del config[k]
        config_json = json.dumps(config)
        for k in js_functions:
            index = config_json.rfind('}')
            config_json = config_json[:index]+', '+k+':'+js_functions[k].strip()+config_json[index:]
        return config_json

    def get_tinymce_config(self, name, attrs):
        config = copy.deepcopy(fields_bundle.settings.FIELDS_BUNDLE_TINYMCE_DEFAULT_CONFIG)
        config.update(self.tinymce)
        # if mce_config['mode'] == 'exact':
        #
        config['mode'] = 'exact'
        config['elements'] = attrs['id']
        config['placeholder'] = attrs.get('placeholder', '')

        config['language'] = None
        config['language_url'] = settings.STATIC_URL + 'vendors/tinymce/langs/fr.js'

        if self.inline:
            config['inline'] = True
            config['content_css'] = None
            config['elements'] = "div_inline_%s" % name

            config['force_br_newlines'] = False
            config['force_p_newlines'] = False
            config['forced_root_block'] = ''

        if config.get('content_css', None):
            content_css_new = []
            for url in config['content_css'].split(','):
                url = url.strip()
                if not is_absolute(url):
                    content_css_new.append(os.path.join(settings.STATIC_URL, url))
                else:
                    content_css_new.append(url)
            config['content_css'] = ",".join(content_css_new)

        if 'external_plugins' in config:

            for key, url in config['external_plugins'].items():
                url = url.strip()
                if not is_absolute(url):
                    config['external_plugins'][key] = os.path.join(settings.STATIC_URL, url)

        return config

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''
        value = smart_unicode(value)
        flatattrs = self.build_attrs(attrs)
        flatattrs['name'] = name


        if self.tinymce and self.tinymce.get('apply_format') == "text":
            value = strip_tags(value).replace('\n', '<br />').replace('\n', '<br />')

        config = {
            'inline': self.inline,
            'type' : 'tinymce',
            'id' : attrs['id'],
            'name' : name,
            'settings' : self.get_tinymce_config(name, attrs)
        }
        flatattrs['data-fields_bundle-html_input'] = self.get_config_json(config)


        if self.inline:

            html = [u"""<div class="fields_bundle-tinymce_inline">
                <div id="div_inline_%s" placeholder="%s">%s</div>
                <div style="display:none;">
                    <textarea%s>%s</textarea>
                </div>
            </div>
            """ % (name, flatattrs.get('placeholder'), mark_safe(value), flatatt(flatattrs), escape(value))]
            return mark_safe('\n'.join(html))

        else:
            html =  ['<textarea%s>%s</textarea>' % (flatatt(flatattrs), escape(value))]
            return mark_safe('\n'.join(html))
