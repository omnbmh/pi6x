pi6x
====
玩转树莓派 本项目基于树莓派A版

- 内置服务
    - NTP
    - rpcbind
    - git
    - Java: 1.8.0, Java HotSpot(TM) Client VM, Oracle Corporation, 25.0-b70
    - openssh

- 扩展服务
    - Nginx 1.2.1 openresty  Nginx + Lua
    - Apache Tomcat 8.0.24
    - Solr 5.5.0 <https://github.com/omnbmh/pi6x/blob/master/docs/solr.md>
    - Nexus <https://github.com/omnbmh/pi6x/blob/master/docs/nexus.md> `非原生 官方的package不支持arm等非标准的linux系统`
    - Mysql 5.5
    - Dnsmasq
    - Samba
    - Motion <https://github.com/omnbmh/pi6x/blob/master/docs/motion.md>  `一款多功能监控软件`

====
- Hardware `存放 关于硬件的资料和代码`
    - CPU:
    - Memory:
    - OS: Linux, 4.1.19+, arm
    - Last Upgrade: 2016-05-12
- Docs `各种文档的聚集地`
    - 初始化树莓派 <https://github.com/omnbmh/pi6x/blob/master/docs/init.md>
    - 备份SD卡 <https://github.com/omnbmh/pi6x/blob/master/docs/backupdisk.md>
    - rpi-update
- Profile
- Webapps
    - webapps/resources 存放 jpg png css js
    - webapps/resources/lib 存放各种引用的库
    - webapps/templates 存放 公共模板


### software env
- django 1.9.1
- Python 2.7


### hardware env
- raspberry pi A
- arduino uno
