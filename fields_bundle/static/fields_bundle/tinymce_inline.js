$(document).ready(function()
{

    $('[data-manage]').each(function(self, token)
    {
        self = $(this);
        token = (Math.random()*1e32).toString(36);
        self.attr('id', token);
        opt = self.data('manage');
        tinymce.init({
            selector: "#"+self.attr('id'),
            inline: true,
            toolbar: "undo redo",
            menubar: false,
            force_br_newlines : false,
            force_p_newlines : false,
            forced_root_block: '',
            setup: function(editor) {
                editor.on('change', function(e) {
                    var value = tinyMCE.activeEditor.getContent({ format : 'text' });
                    opt.input.val(value)
                });
            }
        });
        opt.input = $("#id_"+opt.name);
    });

});