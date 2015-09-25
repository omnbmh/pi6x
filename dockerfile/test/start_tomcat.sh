#!/bin/bash

#Desc:
# start tomcat with docker containerstart.
echo "Start Tomcat ..."
#display contianer ipaddress
ifconfig

# Start tomcat
bash /app/apache-tomcat-8.0.24/bin/catalina.sh run

