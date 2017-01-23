from django.db import models

class TomcatInfo(models.Model):
    tomcat_home = models.CharField(max_length=200)
    tomcat_ip = models.CharField(max_length=20)
    tomcat_http_port = models.CharField(max_length=5)
    ssh_opt = models.CharField(max_length=100)
