###
 # @Description: 拯救PC机apt
 # @Version: 1.0
 # @Autor: lhgcs
 # @Date: 2020-01-07 11:32:15
 # @LastEditors  : lhgcs
 # @LastEditTime : 2020-01-07 11:57:18
 ###

# dpkg之所以能够对每个包的状态了如指掌，完全是因为dpkg数据库--->>/var/lib/dpkg/status
# 这个文本文件中记录了软件仓库中曾经安装过的软件包的安装状态。
# 所以，只需要改动这个文件就能够改变软件包的状态。
# sudo echo "" > /var/lib/dpkg/status
sudo rm -rf /var/lib/dpkg/status
sudo touch /var/lib/dpkg/status

# 删除孤立的软件
sudo apt-get autoremove
# 清理所有软件缓存
sudo apt-get autoclean
sudo apt-get clean
sudo apt-get -f install

# 删除源
# sudo add-apt-repository -r ppa:user/ppa-name
sudo add-apt-repository --remove ppa:whatever/ppa
# 更新源
sudo apt-get update
sudo apt-get upgrade
# sudo tree /var/cache/apt/archives/

# 大小
sudo du -sh /var/log
# 文件总数
sudo du -sm /var/log
# 删除30天之前的旧文件
sudo find /var/log/ -type f -mtime +30 -exec rm -f {} \;

# 打开启动应用管理，设置开机启动
# gnome-session-properties
