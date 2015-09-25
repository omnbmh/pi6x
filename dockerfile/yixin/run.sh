#!/bin/bash
#DESC:
# Start OpenSSH & Tomcat

echo "Starting ..."

# Export Java Path
export JAVA_HOME=/opt/jdk1.7.0_80
export PATH=$PATH:$JAVA_HOME/bin
echo "eport path ok"


# Start Tomcat
echo "starting tomcat ok"
bash /app/apache-tomcat-8.0.24/bin/catalina.sh run

# Start SSH
#echo "starting ssh ok"
#/usr/sbin/sshd -D
