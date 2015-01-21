;$(document).ready(function(){
    // init ui
    $('button').button({
        icons: {
            primary: "ui-icon-gear"
        }
    });
    // load the vote
    $.ajax({
        async:false,
        url:'http://192.168.8.3:8080/sos-api/vote/show_simple.jsonp',
        type:'GET',
        dataType:'jsonp',
        jsonp:'jsoncallback',
        data:{voteId:'1395628957146'},
        timeout: 5000,
        contentType:'application/json;utf-8',
        success:function(data){
            console.log(data);
            $('#vote-title').html(data.result.title);
            var html = [];
            html.push('<ul>');
            for (var i = 0, j=data.result.options.length;i<j;i++){
                var option = data.result.options[i];
                html.push("<li>");
                html.push('<input type="radio" name="vote-option-1395628957146" id="vote-option-356" value="'+option.option_id+'">');
                html.push('<span>');
                html.push(option.content);
                html.push('</span>');
                html.push("</li>")
            }
            html.push('</ul>');
            $('#vote-box').append(html.join(""));
        },
        error:function (jqXHR, textStatus, errorThrown) { 
            alert(textStatus); 
        } 
    });
    $(document).on('click','#tencent-qq-login',function(){
        window.location.href='http://192.168.8.3:8080/sos/open_login?app_key=100002&plat_type=2&redirect_uri=http://192.168.8.102:8888/event54/authorize&state=&scope=';
    });
    $(document).on('click','#sina-weibo-login',function(){
        window.location.href='http://192.168.8.3:8080/sos/open_login?app_key=100002&plat_type=1&redirect_uri=http://192.168.8.102:8888/event54/authorize&state=&scope=';
    });
    $(document).on('click','#anonymous-login',function(){
        //window.location.href='http://192.168.8.102:8080/sos/open_login?app_key=100002&plat_type=1&redirect_uri=http://192.168.8.102:8888/event54/authorize&state=&scope=';
    });
});