# VERSION 2015.09.01
# 变现通 项目组 测试环境 镜像
# use:
# jdk-7u80-linux-x64
FROM centos:5

MAINTAINER dezhichen<dezhichen@creditease.cn>

RUN mkdir -p /opt/jdk1.7.0_80
RUN mkdir -p /app/apache-tomcat-8.0.24
# install java tomcat tar file, docker can auto unzip
#ADD apache-tomcat-8.0.24.tar.gz $APP_PATH
#ADD jdk-7u80-linux-x64.gz $APP_PATH

# add jdk tomcat start_script into image
ADD jdk1.7.0_80 /opt/jdk1.7.0_80
ADD apache-tomcat-8.0.24 /app/apache-tomcat-8.0.24
#ADD run.sh run.sh

# ENV setting
ENV JAVA_HOME /opt/jdk1.7.0_80
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH .:$JAVA_HOME/lib:$JRE_HOME/lib
ENV PATH $PATH:$JAVA_HOME/bin

# fix sshd can't start on centos 5
RUN set -x \
    && ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' \
    && ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''

# set root passwd
RUN echo "root:123456" | chpasswd
    
# open SSH port 22
#EXPOSE 22

# open Tomcat port 8080
#EXPOSE 8080

# default script /root/run
CMD /app/apache-tomcat-8.0.24/bin/startup.sh && /usr/sbin/sshd -D
