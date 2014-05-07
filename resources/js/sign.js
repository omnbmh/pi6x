;$(document).ready(function(){
    $('button').button({
        icons: {
            primary: "ui-icon-gear"
        }
    });
    $("#tabs").tabs({
      beforeLoad: function( event, ui ) {
        ui.jqXHR.error(function() {
          ui.panel.html(
            "Couldn't load this tab. We'll try to fix this as soon as possible. " +
            "If this wouldn't be a demo." );
        });
      }
    });
    $(document).on('click','#tencent-weibo-login',function(){
        window.location.href='api/auth/login';
    });
});