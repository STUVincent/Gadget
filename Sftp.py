# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
通过 SFTP 上传和下载文件到服务器上。
本地需要安装 paramiko 包

# 当前项目: Tools
# 创建时间: 2018/8/8 22:18
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
import paramiko
import os
import time


# 远程 SSH 连接，命令
class SSH(object):
    def __init__(self, hostname, port, username, password):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        self.ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password)

    # 命令传输
    def cmd(self, code):
        """
        :param code:  Linux  命令【部分命令不支持】
        :return:
        """
        _, stdout, stderr = self.ssh.exec_command(code)
        result = stdout.read()
        if not result:
            result = stderr.read()

        # print('\n--------------- {}'.format(code))
        # print(result.decode())
        return result.decode()

    # 关闭SSH
    def close(self):
        self.ssh.close()


# 远程 SFTP 传输文件
class SFTP(object):
    def __init__(self, hostname, port, username, password):
        self.transport = paramiko.Transport(hostname, port)
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    # 将本地文件放到服务器上
    def put(self, source_file, object_path):
        """
        :param source_file:   服务器待提取的文件路径及名称
        :param object_path:   待存放的本地路径
        :return:
        """
        basename = os.path.basename(source_file)
        # 将 source_file  放到服务器 object_file 路径下
        self.sftp.put(source_file, object_path + '/' + basename)
        print('{}  --> {}'.format(source_file, object_path + '/' + basename))

    # 将服务器上的文件拉到本地
    def get(self, source_file, object_path):
        """
        :param source_file:   服务器待提取的文件路径及名称
        :param object_path:   待存放的本地路径
        :return:
        """
        basename = os.path.basename(source_file)  # 文件名
        # 将服务器 source_file 文件 拉到 object_file 路径下
        self.sftp.get(source_file, os.path.join(object_path, basename))

    def close(self):
        self.transport.close()


# 文件夹批量下载操作
def download(ssh, source_path, object_path, dir_path=None):
    """
    :param ssh:  远程 SSH 连接
    :param source_path:  待复制的服务器文件夹路径
    :param object_path:  保存到本地指定的文件夹路径
    :param dir_path:   过程临时路径
    :return:
    """
    # 初始化过程此路径就是源路径
    if dir_path is None:
        dir_path = source_path

    # 查找当前目录下的文件列表及其信息
    ls = ssh.cmd('ls -al %s' % dir_path)

    for file_i in ls.split('\n')[3:]:
        file_i_list = file_i.split()
        if len(file_i_list) > 1:

            # 若为文件直接 打印文件名
            if file_i_list[1] == '1':
                file_path = '{}/{}'.format(dir_path, file_i_list[-1])
                file_size = '{:.2f}M'.format(int(file_i_list[4]) / 1048576)
                file_time = '-'.join(file_i_list[5:8])

                object_path_i = object_path + '\\' + \
                    '\\'.join(dir_path.split('/')[len(source_path.split('/')):])

                # 判断本地文件夹中是否存在此文件， 若无此文件则进入下载
                if not os.path.exists(
                    os.path.join(
                        object_path_i,
                        os.path.basename(file_path))):
                    # 从服务器上下载文件到指定文件夹中
                    sftp.get(file_path, object_path_i)
                    print(
                        file_path,
                        file_size,
                        file_time,
                        ' --> ',
                        object_path_i)

            # 文件夹，进入下一步搜索
            else:
                # print(file_i_list)
                object_path_i = object_path + '\\' + \
                    '\\'.join(dir_path.split('/')[len(source_path.split('/')):]) + \
                    '\\' + file_i_list[-1]

                # 若文件夹不存在则重新创建
                if not os.path.exists(object_path_i):
                    os.mkdir(object_path_i)
                # 进入子级文件夹迭代过程
                download(ssh=ssh,
                         source_path=source_path,
                         object_path=object_path,
                         dir_path=dir_path + '/' + file_i_list[-1])


# ##################################################################################################
if __name__ == '__main__':
    hostname = '192.168.231.131'
    port = 22
    username = 'vincent'
    password = 'vincent'

    linux_ssh = SSH(
        hostname=hostname,
        port=port,
        username=username,
        password=password)

    sftp = SFTP(
        hostname=hostname,
        port=port,
        username=username,
        password=password)

    # 上传文件
    print('\nUpload..........')
    sftp.put(r'C:\Users\Vincent\Desktop\test_1.txt', '/home/vincent/Desktop')
    sftp.put(r'C:\Users\Vincent\Desktop\test_2.txt', '/home/vincent/Desktop')

    # 下载文件  【若文件已存在，则不再重复下载】
    print('\nDownload........')
    download(ssh=linux_ssh, source_path='/home/vincent/Desktop/Temp', object_path=r'C:\Users\Vincent\Desktop\Linux')

    print(u'\n传输结束！' + time.strftime('      %Y-%m-%d %X', time.localtime()))
    sftp.close()
    linux_ssh.close()
