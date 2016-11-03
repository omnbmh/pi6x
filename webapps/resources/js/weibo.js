;(function(window, undefined){
    "use strict";
    var $ = window.jQuery;

    $.ajaxSetup({data:{author:'***'}, cache:false });

    // 模板
    var tmpl ={
        weibo:$.templates('#weibo'),
        head:$.templates('#head')
    }

    var load = function (){
        // 加载可能认识的人
        $.getJSON('api/weibo/other/kownperson',function(data){
            for (var i = 0, j = data.users.length; i<j;i++){
                var user = data.users[i];
                var $html = $(tmpl.head.render(user));
                $('#kown-boxes').append($html);
            }
        });

        $.getJSON('api/weibo/home',function(data){
            for (var i = 0, j = data.statuses.length; i<j;i++){
                var weibo = data.statuses[i];
                var $html = $(tmpl.weibo.render(weibo));
                $('#weibo-boxes').append($html);
            }
        });
    };

    load();

    // 发送微博
    $(document).on('click', "a[action-type='post']", function() {
        var $this = $(this).closest('div.p1_box');
        var text = $("blockquote[e-type='text']",$this).text();
        var img_url = $("img[e-type='img']",$this).attr('e-data');
        console.info(text+img_url);
        $.getJSON('api/weibo/post', {text: text, url: img_url },function(data){
            alert(data);
        });
    });
})(window);
