centos7
Subversion的安装与配置
1.#检查是否安装了低版本的SVN
rpm -qa subversion
2.安装SVN
yum install httpd httpd-devel subversion mod_dav_svn mod_auth_mysql
3.确认已经安装了svn模块
ls /etc/httpd/modules | grep svn
4.验证安装
svnserve --version

sudo apt-get install subversion
创建仓库
svnadmin create /var/svn
修改配置文件/var/svn/conf/svnserve.conf
修改配置文件passwd
killall svnserve
svnserve -d -r /var/svn
