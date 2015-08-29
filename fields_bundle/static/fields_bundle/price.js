

var NAVIGATOR_IS_MOBILE = (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()));




$(document).ready(function(header_fit, datetimepicker) {


    function getCarret(el) {
        var pos;
        if (document.selection) {
            el.focus();
            var sel = document.selection.createRange();
            sel.moveStart('character', -el.value.length);
            var pos = sel.text.length;
        }
        else if (el.selectionStart || el.selectionStart == '0') {
            var pos = el.selectionStart;
        }
        return pos;

    };

    function setCarret(el, start, end) {
        if (document.selection) {
            var sel = document.selection.createRange();
            sel.moveStart('character', start);
        }
        else if (this.createTextRange) {
            var part = el.createTextRange();
            part.move("character", start);
            part.select();
        }
        else if (el.setSelectionRange) {
            el.setSelectionRange(start, end);
        }
        el.focus();
    };

    function getCharPress(e) {
        return String.fromCharCode(window.event ? e.keyCode : e.which);
    }

    function isNumeric(str) {
        return !isNaN(parseInt(str));
    }


    var CURRENCY_PATTERNS = {
        'EUR': { 'format': '%s €', 'locale': 'fr_FR', 'spacing': ' ', 'decimal': ',', 'placeholder': 'EUR' },
        'USD': { 'format': '$%s', 'locale': 'en_US', 'spacing': ',', 'decimal': '.', 'placeholder': 'USD' },
    };

    $('form').delegate('input.price-formated', 'keyup', function(self, oldVal) {
        self = $(this);
        var pos = getCarret(this);
            spaces = 0,
            oldVal = val = $(this).val(),
            range = [],
            decimal = null,
            currency = self.attr('data-currency'),
            currency_patterns = typeof self.attr('data-currency-patterns') != 'undefined' ? $.parseJSON(self.attr('data-currency-patterns')) : CURRENCY_PATTERNS
        ;
        if(!currency in currency_patterns) {
            currency = 'EUR';
        }
        var pattern = currency_patterns[currency];

        val = self.val();
        if($.trim(val) == "") return false;
        val_dec = val.split(pattern.decimal);
        val = val_dec[0].replace(/[^\d]/g, '');
        if(val_dec.length > 1) {
            decimal = val_dec[1].replace(/[^\d]/g, '').slice(0,2);
        }
        if(val.length <= 0) {
            val = 0;
        }
        if(!self.data('spaces') || typeof self.data('spaces') == 'undefined' || val.length <= 3) {
           self.data('spaces', 0);
        }
        var m = 0;
        for(var i=val.length; i>=0; i--) {
            if(val.length > 3 && i < val.length && (m%3==0)) {
                range.push(pattern.spacing+val[i]);
                if(pos >= i) {
                    spaces++;
                }
            }
            else {
                range.push(val[i]);
            }
            m++;
        }
        range.reverse();
        pos += Math.min(1, spaces - self.data('spaces'));
        self.data('spaces', spaces);
        val = $.trim(range.join(''));
        val = (val ? val : 0) + (decimal != null ? pattern.decimal+ decimal : '');
        $(this).val(pattern.format.replace('%s', val));
        setCarret(this, pos, pos);
        return false;
    });

});