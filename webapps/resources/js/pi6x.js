;(function(window, undefined){
    "use strict";
    var $ = window.jQuery;
    // loading tomcat status
    $("[name='tomcat_box'] tr").each(function(idx,emt){
      if(idx != 0){
        var tds = $('td',emt);
        var ip = $(tds[1]).text();
        var port = $(tds[2]).text();
        $.getJSON('api/tomcat_status.json',
        {'ip':ip,'port':port},
        function(data){
            var status = data.status;
            if(status){
              $('span',tds[3]).removeClass('glyphicon-remove');
              $('span',tds[3]).addClass('glyphicon-ok');
              $('span',tds[3]).css('color','green');
            }
          });
        }
      });
  })(window);
