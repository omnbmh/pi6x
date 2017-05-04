### 使用cronolog分割tomcat的catalina.out文件

需要修改catalina.sh文件
原来：
      
      org.apache.catalina.startup.Bootstrap   "$@" start \

      >> "$CATALINA_OUT"   2>&1 &

修改为：

       org.apache.catalina.startup.Bootstrap   "$@" start \

      | /opt/cronolog/sbin/cronolog   "$CATALINA_BASE"/logs/catalina.%Y-%m-%d.out >> /dev/null   2>&1 &



同时注释掉 下面一行

touch "$CATALINA_OUT"

完成之后重起Tomcat就可以了。
