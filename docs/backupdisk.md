树莓派频繁断电 导致sd卡经常无法启动 经常备份下 防止不时之需
备份
dd if=/dev/mmcblk0 of=/path/to/raspberry.2016.img bs=1M
还原
dd bs=1M if=/path/to/raspberry.2016.img of=/dev/mmcblk0

发现本来只是用了2g多的磁盘空间 备份后和sd卡一样的大小 不爽，咋办 可以使用压缩处理下
压缩备份
dd bs=1M if=/dev/mmcblk0 | gzip > /path/to/raspberry.2016.img.gz
压缩还原
gzip -dc /path/to/raspberry.2016.img.gz | dd bs=4M of=/dev/mmcblk0