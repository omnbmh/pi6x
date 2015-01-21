;$(document).ready(function(){
    var selector = {};
    var cnt = window.document;
    $(cnt).on("click","#event-create",function(e){
        $.getJSON("create",{
                title:$("#title-create").val(),
                info:$("#info-create").val(),
                begin_at:$("#at-begin").val(),
                end_at:$("#at-end").val()
            },
            function(data){
                console.log(data);
            });
    });
});