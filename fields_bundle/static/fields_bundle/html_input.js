(function ($)
{
    function fields_bundle_load_html_input($input, config, id)
    {
        if($input[0].fields_bundle_load_html_input_loaded)
        {
            return;
        }
        if ($input.parents('.empty-form').length == 0 &&
            $input.parents('.form-__prefix__').length == 0)
        {
            $input[0].fields_bundle_load_html_input_loaded = true;
            config = $input.data('fields_bundle-html_input');
            if(!config.apply_format)
            {
                config.apply_format = 'html'
            }
            if(config.type == "tinymce")
            {
                var tinymce_config = config['settings'];
                id = tinymce_config['elements'];
                if (tinymce.editors[id])
                {
                    tinymce.editors[id].destroy()
                }
                if (!tinymce.editors[id])
                {
                    tinymce_config.setup = function(editor)
                    {
                        editor.on('change', function(e)
                        {
                            var content = editor.getContent({ format : config.apply_format });
                            var content_text = editor.getContent({ format : 'text' }).replace(/^\s+|\s+$/g, '');
                            if(config.inline)
                            {
                                placeholder = editor.getElement().getAttribute("placeholder");
                                if (typeof placeholder !== 'undefined' && placeholder !== false && content_text == placeholder)
                                {
                                    return;
                                }
                                $input.val(content).change();
                            }
                        });
                        editor.on('init', function(e, placeholder)
                        {
                            placeholder = editor.getElement().getAttribute("placeholder");
                            if (typeof placeholder !== 'undefined' && placeholder !== false)
                            {
                                //var label = new Label;
                                function onFocus()
                                {
                                    var content = editor.getContent({ format : 'text' }).replace(/^\s+|\s+$/g, '');
                                    if(content == '' || content == placeholder)
                                    {
                                        editor.focus();
                                        editor.setContent('');
                                        tinymce.setActive(editor);
                                        editor.focus();
                                        editor.execCommand('mceFocus', false, id);
                                        $(editor.getElement()).click();
                                    }
                                        console.log('onFocus')
                                }

                                function onBlur()
                                {
                                    var content = editor.getContent({ format : 'text' }).replace(/^\s+|\s+$/g, '');
                                    if(content == '')
                                    {
                                        var placeholder_html = '<span class="fields-bundle-html_input-placeholder">'+placeholder+'</span>'
                                        editor.setContent(placeholder_html);
                                        editor.getElement().innerHTML = placeholder_html
                                    }
                                        console.log('onBlur')
                                }
                                //tinymce.DOM.bind(label.el, 'click', onFocus);
                                editor.on('focus', onFocus);
                                editor.on('blur', onBlur);
                                onBlur();
                            }
                        });
                    }
                    var instance = tinymce.init(tinymce_config);
                }
            }
        }
    }

    $(function ()
    {
        $('[data-fields_bundle-html_input]').each(function(i, self)
        {
            fields_bundle_load_html_input($(self));
        });
        // $(document).on('mousenter', '[data-fields_bundle-html_input]', function(self)
        // {
        //     fields_bundle_load_html_input($(this));
        // });

        $(document).on('mouseup', function(self)    {
            setTimeout(function()
            {
                // We have to wait until the inline is added
                $('[data-fields_bundle-html_input]').each(function(i, self)
                {
                    fields_bundle_load_html_input($(self));
                });
            }, 0);
        });
    });



    /*$(function ()
    {
        // initialize the TinyMCE editors on load
        $('.tinymce').each(function () {
            initTinyMCE($(this));
        });

        // initialize the TinyMCE editor after adding an inline
        // XXX: We don't use jQuery's click event as it won't work in Django 1.4
        document.body.addEventListener("click", function(ev)
        {
            if(!ev.target.parentNode || ev.target.parentNode.className.indexOf("add-row") === -1) {
                return;
            }
            var $addRow = $(ev.target.parentNode);
            setTimeout(function()
            {  // We have to wait until the inline is added
                $('textarea.tinymce', $addRow.parent()).each(function () {
                    initTinyMCE($(this));
                });
            }, 0);
        }, true);
    });*/

}(django && django.jQuery || jQuery));
// }
// if(typeof tinymce == 'undefined' )
// {
//     var script = document.createElement('script');
//     script.src = "//tinymce.cachefly.net/4.2/tinymce.min.js";
//     var head = document.getElementsByTagName('head')[0], done = false;
//     script.onload = script.onreadystatechange = function()
//     {
//         if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete'))
//         {
//             done = true
//             // callback function provided as param
//             fields_bundle_load_html_input();
//             console.log('load')
//             script.onload = script.onreadystatechange = null;
//             head.removeChild(script);
//         };
//     };
//     head.appendChild(script);
// }
// else
// {
//     fields_bundle_load_html_input();
// }