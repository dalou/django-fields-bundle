
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt
from tinymce.widgets import get_language_config, TinyMCE as TinyMCEInput
import tinymce.settings


class HtmlInput(TinyMCEInput):

    def __init__(self, content_language=None, attrs=None, tinymce=None, placeholder=None):

        super(HtmlInput, self).__init__(attrs=attrs, mce_attrs=tinymce)



    def _media(self):
        return forms.Media(js=[
            "//tinymce.cachefly.net/4.2/tinymce.min.js"
        ])



    def get_mce_config(self, attrs):

        mce_config = tinymce.settings.DEFAULT_CONFIG.copy()
        # mce_config.update(get_language_config(self.content_language))
        # if tinymce.settings.USE_FILEBROWSER:
        #     mce_config['file_browser_callback'] = "djangoFileBrowser"
        mce_config.update(self.mce_attrs)
        if mce_config['mode'] == 'exact':
            mce_config['elements'] = attrs['id']

        mce_config['language'] = None
        mce_config['language_url'] = settings.STATIC_URL + 'vendors/tinymce/langs/fr.js'

        return mce_config

    def render(self, name, value, attrs=None):


        original_render = super(HtmlInput, self).render(name, value, attrs=attrs)
        html = u"""
            %s
            <script>
                var load_tinymce = function()
                {
                    (function ($)
                    {
                        //function initTinyMCE($e) {
                        var $e = $("#%s");
                        if ($e.parents('.empty-form').length == 0)
                        {
                            // Don't do empty inlines
                            var mce_conf = $.parseJSON($e.attr('data-mce-conf'));
                            /* var id = $e.attr('id');
                            if ('elements' in mce_conf && mce_conf['mode'] == 'exact')
                            {
                                mce_conf['elements'] = id;
                            }*/
                            if ($e.attr('data-mce-gz-conf'))
                            {
                                tinyMCE_GZ.init($.parseJSON($e.attr('data-mce-gz-conf')));
                            }
                            var id = mce_conf['elements'];
                            //mce_conf['selector'] = '#'+id;
                            //mce_conf['elements'] = null;
                            if (!tinymce.editors[id])
                            {

                                tinymce.init(mce_conf);
                            }
                        }
                        //}

                        /*$(function () {
                            // initialize the TinyMCE editors on load
                            $('.tinymce').each(function () {
                                initTinyMCE($(this));
                            });

                            // initialize the TinyMCE editor after adding an inline
                            // XXX: We don't use jQuery's click event as it won't work in Django 1.4
                            document.body.addEventListener("click", function(ev) {
                              if(!ev.target.parentNode || ev.target.parentNode.className.indexOf("add-row") === -1) {
                                return;
                              }
                              var $addRow = $(ev.target.parentNode);
                              setTimeout(function() {  // We have to wait until the inline is added
                                $('textarea.tinymce', $addRow.parent()).each(function () {
                                  initTinyMCE($(this));
                                });
                              }, 0);
                            }, true);
                        });*/

                    }(django && django.jQuery || jQuery));
                }
                if(typeof tinymce == 'undefined' )
                {
                    var script = document.createElement('script');
                    script.src = "//tinymce.cachefly.net/4.2/tinymce.min.js";
                    var head = document.getElementsByTagName('head')[0], done = false;
                    script.onload = script.onreadystatechange = function() {

                        if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete'))
                        {
                            done = true
                            // callback function provided as param
                            load_tinymce();
                            console.log('load')
                            script.onload = script.onreadystatechange = null;
                            head.removeChild(script);
                        };
                    };
                    head.appendChild(script);
                }
                else
                {
                    load_tinymce();
                }
            </script>
        """ % (original_render, attrs['id'])
        return mark_safe(html)


class InlineHtmlInput(HtmlInput):

    def get_mce_config(self, attrs):
        print attrs.get('placeholder')
        mce_config = super(InlineHtmlInput, self).get_mce_config(attrs)
        mce_config['inline'] = True
        mce_config['elements'] = "div_inline_%s" % attrs['name']

        mce_config['force_br_newlines'] = False
        mce_config['force_p_newlines'] = False
        mce_config['forced_root_block'] = ''

        return mce_config

    def render(self, name, value, attrs=None):
        print attrs.get('placeholder')

        original_render = super(InlineHtmlInput, self).render(name, value, attrs=attrs)

        html = u"""<div class="fields_bundle-tinymce_inline">
            <div id="div_inline_%s" placeholder="%s">%s</div>
            <div style="display:none;">
                %s
            </div>
        </div>""" % (name, "TEST",  value, original_render)

        return mark_safe(html)