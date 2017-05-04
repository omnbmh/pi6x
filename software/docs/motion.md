
- 安装
    - motion 监控软件 mplayer 用于测试摄像头 (如果安装不了的，可以先 `sudo apt-get update` 一下)
    ｀sudo apt-get install motion mplayer｀
    - 开启摄像头 `sudo rasps-config` Enable Camera -> enable

- 配置
    - 安装完成后，配置文件一般在 `/etc/motion/motion.conf`
    - `sudo vi /etc/motion/motion.conf`
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
    - `motion -n`

- 如果你使用的[红外]摄像头模块 这会还不能工作 motion默认是不支持树莓派的摄像头模块的
- 下载一个修改包 `motion-mmal.tar.gz` 百度云盘 `http://pan.baidu.com/s/1bKwkoA`
- 解压 `tar zxvf motion-mmal.tar.gz`
```
#sudo mv motion /usr/bin/motion
#sudo mv motion-mmalcam.conf /etc/motion.conf
```
- 注意这里 配置文件复制到了 `/etc/motion.conf` 目前用Service方法启动 默认找这个文件 目前还没找到怎么改动到 `/etc/motion/motion.conf`
- 重新修改配置文件 按一下修改 其他默认就可以
```
daemon on
width 1024
height 768
webcontrol_localhost off
ffmpeg_output_movies on
ffmpeg_video_codec msmpeg4
```
- 启动报错了 却少依赖包 以下是我碰到的error
```
motion: error while loading shared libraries: libavformat.so.53: cannot open shared object file: No such file or directory
```
- 使用下面的命令 下载缺少的包
- 命令一 ： 网上找的
```
sudo apt-get install -y libjpeg62 libjpeg62-dev libavformat53 libavformat-dev libavcodec53 libavcodec-dev libavutil51 libavutil-dev libc6-dev zlib1g-dev libmysqlclient18 libmysqlclient-dev libpq5 libpq-dev
```
- 命令二：我自己试了下 其他的已经内置 妈蛋 最新的系统怎么装 都不行  原来是缺少 `ffmpeg`
- `sudo apt-get install ffmpeg`

- 挂载个U盘 树莓派的SD卡稳定性不高 建议挂个U盘或者硬盘
   `sudo mount -t auto -o uid=pi,gid=pi,umask= /dev/sda4 /mnt/USB_FLASH`

- 其他
    - 配置网页：http://yourip:8080
    - 监控网页：http://yourip:8081
    - motion官方wiki中的Config options: <http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome>
