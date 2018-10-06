# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
打印指定文件夹下所有文件名

# 当前项目: Tools
# 创建时间: 2018/8/8 22:00 
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
import os
import time
import argparse


#  把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
def time2str(timestamp):
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)


# 打印指定路径下的 各文件信息
def print_file_list(path='.', txt_path=None):

    path = os.path.abspath(path)

    print('Search Path:  【{}】'.format(path))
    # 若没有指定保存文件名， 直接以搜索文件夹名称作为文件名
    if txt_path is None:
        txt_path = os.path.basename(path)

    f_txt_path = '{}_FileList.txt'.format(txt_path)
    f_txt = open(f_txt_path, 'w', encoding='utf8')
    print(' '*100, file=f_txt)

    root = []  # 根目录
    dirs = []  # 文件夹名称
    files = []  # 文件名称

    for root_i, dirs_i, files_i in os.walk(path, topdown=True):
        root.append(root_i)
        dirs.append(dirs_i)
        files.append(files_i)

    raw_layer = len(path.split(os.sep)) - 1

    # 文件夹大小
    folder_size = 0

    for i, root_i in enumerate(root):

        diff_layer = len(root_i.split(os.sep)) - raw_layer

        print(u'{}└-- {}'.format('    ' * (diff_layer - 1), root_i), file=f_txt)

        for ii, file_i in enumerate(files[i]):
            f_path = os.path.join(root_i, file_i)

            try:
                # 大小  KB
                f_size = os.path.getsize(f_path)/1024
                folder_size += f_size
            except:
                f_size = -1
            # # 创建日期
            # f_ctime = time2str(os.path.getctime(f_path))

            try:
                # 修改日期
                f_mtime = time2str(os.path.getmtime(f_path))
            except:
                f_mtime = 'None'
            if ii < len(files[i])-1:
                print(u'{}├-- {}    【{:.2f} KB   {}】'.format('    ' * diff_layer, file_i, f_size, f_mtime),
                      file=f_txt)
            else:
                print(u'{}└-- {}    【{:.2f} KB   {}】'.format('    ' * diff_layer, file_i, f_size, f_mtime),
                      file=f_txt)

    # 文件指针移动到文件头
    f_txt.seek(0)
    print('{}  Folder Size:【{:.3f} MB】'.format(path, folder_size/1024), file=f_txt)

    print('Search Over!  Folder Size:【{:.3f} MB】  Result Save Path:  【{}】'.format(folder_size/1024,
                                                                                  os.path.abspath(f_txt_path)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
        文件搜索脚本
        """)

    # 训练样本文件名称
    parser.add_argument('-f', '--folder', default='.', help='待搜索的文件夹路径, 默认为当前目录')

    args = parser.parse_args()

    print_file_list(args.folder)
