$(document).ready(function() {




    $(document).on('mouseenter', '.fields_bundle-media_input', function(self, only_file, authorized_types, modal, inputs, name)
    {
        if(this.fields_bundle_media_input_active)
        {
            return;
        }
        this.fields_bundle_media_input_active = true;

        self = $(this);
        only_file = self.hasClass('fields_bundle-media_input-only_file');
        authorized_types = self.data('fields_bundle-media_input-authorized_types');
        modal = self.find('.fields_bundle-media_input-modal');
        inputs = $(self.data('inputs'))
        name = self.data('name')


        var $form = $(inputs.find('input').eq(0)[0].form);
        if($form.attr('enctype') != 'multipart/form-data')
        {
            $form.attr('enctype', 'multipart/form-data');
        }
        self.on('click', '.fields_bundle-media_input-remove', function()
        {
            self.find('.fields_bundle-media_input-change').change();
            self.find('input[type=checkbox]').eq(0).prop('checked', true)
        });
        modal.on('click', '.fields_bundle-media_input-remove', function()
        {
            self.find('.fields_bundle-media_input-media').removeClass('active');
            self.find('.fields_bundle-media_input-empty').addClass('active');
            self.find('.fields_bundle-media_input-embed').val('');
            inputs.find('input[type=checkbox]').eq(0).prop('checked', true)
        });

        // self.on('click', '.fields_bundle-media_input-embed', function()
        // {
        //     self.find('textarea').show()
        //     // self.find('.fields_bundle-media_input-media').addClass('active');
        //     // self.find('.fields_bundle-media_input-empty').removeClass('active');
        //     self.find('input[type=checkbox]').eq(0).prop('checked', false).change();
        // });

        /* validate embed code */
        modal.on('paste', '.fields_bundle-media_input-add-embed', function(e, input)
        {
            input = $(this);
            setTimeout(function(e) {

                inputs.find('textarea').attr('name', name).val(input.val());
                inputs.find('input[type=file]').removeAttr('name');
                inputs.find('input[type=checkbox]').eq(0).prop('checked', false);

                self.find('.fields_bundle-media_input-preview').html(input.val());
                self.find('.fields_bundle-media_input-media').addClass('active');
                self.find('.fields_bundle-media_input-empty').removeClass('active');
            }, 0);
            $.magnificPopup.close();
        });

        /* click to add image from input file */
        modal.on('click', '.fields_bundle-media_input-add-image', function()
        {
            inputs.find('input[type=file]').click();
            return false;
        });

        /* Upload image receive */
        inputs.on('change', 'input[type=file]', function(e)
        {
            var files = this.files;
            if (!files || files.length == 0)
            {
                $(this).val(null);
                return false;
            }
            if (files.length > 1) {
                console.log("Not supporting more than 1 file");
            }
            var file = files[0];
            if(!file.type.match(/image.*/)) { }
            else
            {
                inputs.find('textarea').removeAttr('name');
                inputs.find('input[type=file]').attr('name', name);
                var reader = new FileReader();
                reader.onload = (function(newFile)
                {
                    return function(e) {
                        self.find('.fields_bundle-media_input-preview').html('<img src="'+e.target.result+'"/>');
                        self.find('.fields_bundle-media_input-media').addClass('active');
                        self.find('.fields_bundle-media_input-empty').removeClass('active');
                        inputs.find('input[type=checkbox]').eq(0).prop('checked', false);
                        //APPLY($input, $input_cropped);
                    };
                })(file);
                var ret = reader.readAsDataURL(file), canvas = document.createElement("canvas");
                ctx = canvas.getContext("2d");
                self.onload = function()
                {
                    ctx.drawImage($input_cropped.parent(), 100, 100);
                }
            }
            $.magnificPopup.close();
        });
    });



});