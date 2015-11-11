
# from tinymce.models import HTMLField as TinyMceHTMLField

from django.db import models
from ..forms import HtmlInput


# class HTMLField(TinyMceHTMLField):
#     pass

class HTMLField(models.TextField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """
    def formfield(self, **kwargs):
        defaults = { 'widget': HtmlInput }
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        # if defaults['widget'] == admin_widgets.AdminTextareaWidget:
        #     defaults['widget'] = tinymce_widgets.AdminTinyMCE

        defaults['widget'] = HtmlInput(attrs={'placeholder': self.verbose_name})

        return super(HTMLField, self).formfield(**defaults)

class HtmlField(HTMLField):
    pass

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fields_bundle\.fields\.HtmlField"])
except ImportError:
    pass