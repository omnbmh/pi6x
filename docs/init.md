* 烧录系统 实用的是2016-05-27的镜像
  * 推荐新手使用 NOOBS 安装 比较傻瓜式 Go To `https://www.raspberrypi.org/downloads/noobs/` 下载最新的系统 此处不要纠结 一定是最新的好
  * 参考安装文档 `https://www.raspberrypi.org/help/noobs-setup/` 英文不好的 页面有安装视频 😂 你怎么不去死呀
  * 我下载的是 NOOBS_v1_9_2.zip
  * 下载 SD Formatter 格式化SD卡 格式化吼SD卡的数据会丢失 请先备份
  * Windows
  * 下载地址 `https://www.sdcard.org/downloads/formatter_4/eula_windows/SDFormatterv4.zip`
  * Mac OS
  * 下载地址 `https://www.sdcard.org/downloads/formatter_4/eula_mac/SDFormatter_4.00B.pkg`
  * 安装完成后 解压 `NOOBS_v1_9_2.zip` 到 SD 卡中
  * 将卡插入树莓派 启动 选择 Raspbian 系统进行安装 这里我就不在啰嗦了 安装界面写的细致

* 配置树莓派

* 修改键盘布局
  * 树莓派默认是英式键盘设置(你若❤️英，便是米旗)，不然要改成美式通用键盘
  *  `#sudo dpkg-reconfigure keyboard-configuration`
  * 选择 Generic 101-key PC -> Other -> English (US) -> English(US, alternative international)
  * #sudo reboot
  * 现在你可以放肆的使用你的 Made in china 键盘了

* 修改时区
  * 只在树莓派上找到了上海的时区 没有Beijing
  * `#sudo dpkg-reconfigure tzdata`
  * 选择 Asia -> Shanghai
  * 输出 Current default time zone: 'Asia/Shanghai'

* 修改软件源
  * 此处不建议修改。由于系统默认的源在国外，大部分国内（墙外用户自便）用户更新软件的时候，速度比较慢，自测官方源还可以，速度能接受
  * 编辑 /etc/apt/source.list 文件
  * `#sudo vi /etc/apt/source.list`
  ``` code
  # SourceList - http://www.raspbian.org/RaspbianMirrors
  #Tsinghua University Network Administrators Unreachable as of 15-may-2015
  deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi
  deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi
  #Dalian Neusoft University of Information
  deb http://mirrors.neusoft.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi
  deb-src http://mirrors.neusoft.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi
  #University of Science and Technology of China (最近在使用 比较快)
  deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main non-free contrib
  deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main non-free contrib
  ```
* 无线网络配置
  * 我的路由器只有两个LAN口，为了节约还是使用wifi吧，建议使用免驱的无线网卡(新的板子自带了wifi和bluetooth)，这样我的树莓派也自由了，省的每天推个线,如果再配上个充电宝，就能移动使用了
  * 执行 `lsusb` 查看是否加载了无线网卡
  ``` code
  Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp.
  Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
  Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.
  Bus 001 Device 004: ID 0cf3:1006 Atheros Communications, Inc. TP-Link TL-WN322G v3 / TL-WN422G v2 802.11g [Atheros AR9271]
  ```
  * `Bus 001 Device 004` 是我的网卡
  * 执行 `ifconfig` 查看下无线网开是否正常工作，因为还没有配置无线网络,这会应该是没有IP的(未连接)
  ```
  wlan0   Link encap:Ethernet  HWaddr 54:e6:fc:0b:67:26  
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
  ```
  * 还不错无线网卡工作正常，接下来我们来编辑下 `sudo vi /etc/network/interfaces` 修改前先备份下 `sudo cp /etc/network/interfaces /etc/network/interfaces20160609`
  * 默认的文件内容
  ```
  auto lo

  iface lo inet loopback
  iface eth0 inet dhcp
      pre-up /etc/firewall-openvpn-rules.sh

  allow-hotplug wlan0
  iface wlan0 inet manual
  wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
  iface default inet dhcp
  ```
  * 说明下参数含义
  ```
  auto lo  //表示使用localhost
  iface eth0 inet dhcp  //表示如果有网卡ech0, 则用dhcp获得IP地址 (这个网卡是本机的网卡，而不是WIFI网卡)
  auto wlan0   //表示如果有wlan设备，使用wlan0设备名
  allow-hotplug wlan0 //表示wlan设备可以热插拨
  iface wlan0 inet dhcp //表示如果有WLAN网卡wlan0 (就是WIFI网卡), 则用dhcp获得IP地址
  wpa-ssid "YourWifiName"  //表示连接SSID名为YourWifiName的WIFI网络。
  wpa-psk "YourWifiPassword" //表示连接WIFI网络时，使用wpa-psk认证方式，认证密码是YourWifiPassword。
  ```
  * 方法一 直接修改 `/etc/network/interfaces` 文件
    * 注释掉
    ```
    ...
    wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
    ```
    * 增加
    ```
    wpa-ssid "YourWifiName"
    wpa-psk "YourWifiPassword"
    ```

* 远程连接 有了树莓派 我们总不能一值连着个显示器 拖着个键鼠
  * 方案一 SSH 默认已经开启 用的也是最多的
  * 方案二 xrdp 方便Windows系统使用
    ```
    sudo apt-get update
    sudo apt-get install xrdp
    ```
    * 打开 Windows 的 远程桌面连接 输入 `your pi's ip:1`
  * 方案二 tinyvnc 通用方案
    * 安装软件
    ```
    sudo apt-get update
    sudo apt-get install tightvncserver
    ```
    * 启动服务 运行下面的命令
    * `vncserver :1` 然后输入链接密码 要记住 使用客户端链接的时候要用
    * 在Windows/Linux/Unix客户端使用 `your pi's ip:1` 进行连接 可以使用 [VNCViewer](http://www.realvnc.com "www.realvnc.com")
    * 使用MAC OS内置的VNC应用访问
      * Finder -> 前往 -> 连接服务器... 输入 `vnc://your pi's ip:5901` 后面的端口号根据实际情况填写

- 常用命令
  - `sudo service --status-all` 检测服务状态
