pi6x
====

玩转树莓派 本项目基于树莓派A版



Hardware
CPU:
Memory:
OS Last Upgrade: 2016-05-12

初始化树莓派
备份SD卡

内置服务
NTP
rpcbind
git
java
openssh


使用之提供服务
Tomcat
Nexus - 官方的package不支持arm等非标准的linux系统
参考 http://stackoverflow.com/questions/28785464/how-to-fix-missing-platform-binary-nexus-2-11-2-03
Mysql
Samba
Nginx
openresty  Nginx + Lua
Nginx Version 1.2.1
Apache Tomcat 8.0.24
Java 1.8.0
Mysql 5.5




### software env
--django 1.9.1
--Python 2.7 - 相对于python3 来说 python2 更具挑战性
Installed /Library/Python/2.7/site-packages/pip-8.0.2-py2.7.egg
pip install django-bootstrap-toolkit ... Successfully installed django-bootstrap-toolkit-2.15.0


### hardware env
--raspberry pi A
--arduino uno

dir-profile

dir-hardware
存放 关于硬件的资料和代码

dir-webapps
webapps/resources 存放 jpg png css js
webapps/resources/lib 存放各种引用的库
webapps/templates 存放 公共模板
webapps/*_app 各种子爱破

dir-docs 
各种文档的聚集地
