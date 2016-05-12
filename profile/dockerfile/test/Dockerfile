# VERSION 2015.07.31
FROM centos:5

# sign
MAINTAINER c8d8z8@gmail.com

# ENV setting
ENV APP_PATH /app

RUN mkdir -p "$APP_PATH"
# install java tomcat tar file auto unzip
ADD ./software/apache-tomcat-8.0.24.tar.gz $APP_PATH
ADD ./software/jdk-7u80-linux-x64.gz $APP_PATH

WORKDIR $APP_PATH
# fix sshd can't start
RUN set -x \
    && ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' \
    && ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''

CMD ["/usr/sbin/sshd", ""]
