/**
 * jQuery money plugin by dezhichen@creditease.cn
 */
; (function($) {
    $.extend({
        money: {
            format: function(number) {
                number = number.toString();
                var arrStr = number.split('.'),
                floatPart = arrStr[1],
                step = 3,
                len = 0;
                number = arrStr[0];
                len = number.length;
                if (len > step) {
                    var c1 = len % step,
                    c2 = parseInt(len / step),
                    arr = [],
                    first = number.substr(0, c1);
                    if (first !== '') {
                        arr.push(first);
                    }
                    for (var i = 0; i < c2; i++) {
                        arr.push(number.substr(c1 + i * step, step));
                    }
                    number = arr.join(',');
                }
                if(typeof(floatPart) === 'undefined'){
                  return number;
                }
                return number + '.' + floatPart;
            }
        }
    });
    $.extend({
        formatMoney: function(number) {
            return $.money.format(number);
        }
    });
})(jQuery);