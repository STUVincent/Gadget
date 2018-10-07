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
