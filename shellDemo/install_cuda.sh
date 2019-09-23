#!/bin/bash

### 
# @Description: 安装cuda(在RK3399上没成功)
 # @Version: 1.0
 # @Autor: lhgcs
 # @Date: 2019-08-26 14:37:10
 # @LastEditors: lhgcs
 # @LastEditTime: 2019-08-26 14:48:24
 ###


# 方法1：下载deb再安装
# wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/ppc64el/cuda-repo-ubuntu1804_10.1.168-1_ppc64el.deb
# sudo dpkg -i cuda-repo-ubuntu1804_10.1.168-1_ppc64el.deb


# 方法2：通过命令安装
# 添加密钥
# sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/ppc64el/7fa2af80.pub

# 更新本地trusted数据库，删除过期没用的key
apt-key update 
# 列出已保存在系统中key
apt-key list  
# apt-key add keyname #把下载的key添加到本地trusted数据库中。
# apt-key del keyname #从本地trusted数据库删除key。 

sudo apt-get autoremove
sudo apt-get update
# 安装
sudo apt-get install cuda