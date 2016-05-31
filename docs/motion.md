
- 安装
    - motion 监控软件 mplayer 用于测试摄像头 (如果安装不了的，可以先 `sudo apt-get update` 一下)
    ｀sudo apt-get install motion mplayer｀
    - 开启摄像头 `sudo rasps-config` Enable Camera -> enable

- 配置
    - 安装完成后，配置文件一般在 `/etc/motion/motion.conf`
    `sudo vi /etc/motion/motion.conf`
    找到
    ``` ini
    control_localhost on
    webcam_localhost on
    ```
    修改为
    ``` ini
    control_localhost off
    webcam_localhost off
    ```
    - 参数配置详解
    - daemon off
    最好这项还是选off，否则运行motion后，就会直接在后台运行，需要用top命令查看出motion的进程号（pid），然后再手动kill掉这个进程。
    - locate on
    设置探测到图像中有运动时，把运动区域用矩形框起来。
    - ffmpeg_cap_new on
    在检测到运动时，用视频纪录下来。
    - ffmpeg_video_codec msmpeg4
    设定视频的编码器

- 运行
    `motion -n`

- 挂载个U盘
   `sudo mount -t auto -o uid=pi,gid=pi,umask= /dev/sda4 /mnt/32GB_USB_FLASH`

- 其他
    - 配置网页：http://192.168.99.53:8080
    - 监控网页：http://192.168.99.53:8081
    - motion官方wiki中的Config options: <http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome>
