# encoding: utf-8
import re
import os
import logging
import locale
import json
import datetime, time


from django import forms
from django.conf import settings
from django.db.models import CharField
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

class IconField(forms.CharField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = IconInput(attrs={'placeholder': '#xxxxxx'})
        super(IconField, self).__init__(*args, **kwargs)



class IconInput(forms.widgets.TextInput):

    class Media:
        css = {
            'all': (
                # settings.STATIC_URL + 'fonts/icomoon/style.css',
                # 'https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css',
            )
        }

    # currency = DEFAULT_CURRENCY

    def __init__(self, *args, **kwargs):

        self.styles = kwargs.pop('styles')
        # if 'currency' in kwargs:
        #     self.currency = kwargs['currency']
        #     del kwargs['currency']
        super(IconInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        root = settings.DJANGO_ROOT

        id = str(time.time()).replace('.', '')

        html = """<style>

            .fields_bundle-icon-widget {
                color:rgb(102, 71, 30); margin:5px; text-decoration: none; cursor: pointer;   display: inline-block;
                font-size: 21px;
                transition: all 0.4s ease-out;
            }
            .fields_bundle-icon-widget:hover {
                text-decoration: none; color:rgb(30, 31, 102);   display: inline-block;
                transition: all 0.4s ease-out;
            }
            .fields_bundle-icon-widget.active {
                color:green; font-size: 25px; font-weight: bold;
            }

        </style>
        <div id="icons-%s">
            <div style="" class="tabs">""" % id

        for title, local_path, path, classname, prefix in self.styles:
            html += """<link href="%s" rel="stylesheet">""" % (path)

        tabs = "<ul>"
        contents = ""

        i = 1
        for title, local_path, path, classname, prefix in self.styles:
            filec = open(os.path.join(root, local_path), 'rb').read()
            filec = filec.replace(r'\s','')

            # title = re.search(r"@font-face\{.+font-family:([\'\"\d\w\-\s]+)\;", filec)
            # title = title.group(1) if title else "Icons"
            # title = title.strip().strip("'").strip('"').strip()

            tabs += """<li><a href="#tab-%s-%s">%s</a></li>""" % (id, i, title)
            contents += """<div id="tab-%s-%s">"""  % (id, i)
            for item in re.finditer(
                r"\.(%s[\w\-\.]+)\:before" % classname,
                filec
            ):
                classname = item.group(1)
                classname = prefix + ' ' + classname
                contents += """<a class="fields_bundle-icon-widget %s" data-value="%s"><i class="%s"></i></a>""" % (
                    "active" if value == classname else "",
                    classname,
                    classname
                )
            contents += "</div>"
            i += 1

        tabs += "</ul>"
        html += tabs + contents

        html += """</div>
                %(inherit)s
            </div>
            <script type="text/javascript">
                $(document).ready(function() {

                    $( "#icons-%(id)s > div.tabs" ).tabs();
                    $(document).on('click', '#icons-%(id)s .fields_bundle-icon-widget', function() {
                         $('.fields_bundle-icon-widget.active').removeClass('active')
                         $(this).addClass('active');
                         $('#icons-%(id)s input').val($(this).data('value'))
                    });
                });
            </script>
        """ % {
            'inherit' : super(IconInput, self).render(name, value, attrs=attrs),
            'id': id
        }
        return mark_safe(html)
