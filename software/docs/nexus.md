Nexus 2.13 的安装和配置

准备：
sudo apt-get install oracle-java8-jdk
下载 nexus-2.13.0-01-bundle.tar.gz 地址：http://www.sonatype.com/download-oss-sonatype

解压到/usr/local
#tar zxvf nexus-2.13.0-01-bundle.tar.gz

切换到 /usr/local/nexus-2.13.0 接下来我们启动试一下

#./bin/nexus
Missing platform binary: /usr/local/nexus-2.13.0-01/bin/../bin/jsw/linux-armv6l-32/wrapper

报错了,官方的package不支持arm等非标准的linux系统，怎整愁死我啦，google了一下，发现了解决方案，参考：http://stackoverflow.com/questions/28785464/how-to-fix-missing-platform-binary-nexus-2-11-2-03

主要步骤：
1.从http://wrapper.tanukisoftware.com/doc/english/download.jsp下载arm版的JSW(Java Service Wrapper) 下载 Linux－armel－3.5.29 的 32-bit 的 Community 版,文件名:wrapper-linux-armel-32-3.5.29.tar.gz
2.解压 wrapper-linux-armel-32-3.5.29.tar.gz
3.复制 bin 下面的所有的文件 到 nexus目录下/bin/jsw/linux-armv6l-32 目录linux-armv6l-32需要新建

👌我们再启动下试试
Usage: ./bin/nexus { console | start | stop | restart | status | dump }
#./bin/nexus start
Starting Nexus OSS...
Failed to start Nexus OSS.

启动失败了，查看日志 syslog 有如下日志
Unable to write to the configured log file: logs/wrapper.log
启动的时候  nexus 不推荐使用root用户 那我们使用默认pi用户 给目录 加上权限 /usr/local/nexus-2.13.0-01 另外发现 /usr/local/sonatype-work 这个目录不存在 需要手动创建 并给pi用户权限

再来  启动

#./bin/nexus start
Starting Nexus OSS...
Started Nexus OSS.

启动的时间有点长 大概3-5分钟左右 喝点水 访问 http://＊.*.*.*:8081/nexus/ 😄成功了 由于树莓派的sd卡的容易坏，并且存储也不大，建议可以把库目录放在u盘或者硬盘里面
