Gadget
===========================
`python` 编写的一些小工具

|Author|Vincent|
|---|---|
|E-mail|stuvincent@163.com|

***************************
## 目录
* [打印文件列表](#打印文件列表 'FileList.py')
* [上传下载文件](#上传下载文件 'Sftp.py')
* [MySQL常用操作](#MySQL常用操作 'mysql.py')
* [API接口调试](#API接口调试 'HTML_Web')
* [Docker常用命令](#Docker常用命令 'Docker')
*************************** 

打印文件列表
------------------------------
`FileList.py` 打印指定文件夹下所有文件信息列表，并保存到脚本所在路径下

```Bash
python FileList.py -f C:\Users\Vincent\Desktop\Gadget
```

![](/img/FileList脚本运行.JPG  'FileList脚本运行.JPG')

![](/img/FileList脚本运行结果.JPG 'FileList脚本运行结果.JPG')

上传下载文件
------------------------------
`Sftp.py` 通过 SFTP 上传和下载文件到服务器上。本地需要安装 paramiko 包。

```Bash
python Sftp.py
```

![](/img/Sftp脚本运行.JPG  'Sftp脚本运行.JPG')

MySQL常用操作
------------------------------
`mysql.py` 封装 MySQL 一些常用的操作，依赖包：pymysql、prettytable(可视化)

```Bash
python mysql.py
```

API接口调试
------------------------------
Python + Flask + HTML 简单的网页界面API接口调试工具
其中 VirtualServers.py 是虚拟后台服务器
Client.py 是调试的主程序 
![](/img/接口调试界面.JPG  '接口调试界面.JPG')

Docker常用命令
------------------------------
![](/img/Docker.jpg  'Docker.jpg')