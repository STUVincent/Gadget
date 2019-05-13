# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
查询指定文件夹下各文件、文件夹信息
"""
import os


#  把文件大小 xx B 转换成对应的最佳显示方式
def _size_h(size):
    if size >= 1024*1024*1024:
        return "{:.1f}GB".format(size/(1024*1024*1024))
    elif size >= 1024*1024:
        return "{:.1f}MB".format(size/(1024*1024))
    elif size >= 1024:
        return "{:.1f}KB".format(size/1024)
    else:
        return "{:.0f}B".format(size)


# 查询文件夹中有多少个文件并计算总大小
def _get_folder_size(folder_path):
    f_size = 0
    f_num = 0
    for root_i, _, files_i in os.walk(folder_path, topdown=True):
        for file_ii in files_i:
            f_size += os.path.getsize(os.path.join(root_i, file_ii))
            f_num += 1
    return f_num, f_size


# 打印指定路径下的 各文件信息  
def print_folder_info(path='.', display_layer=3, url="http://192.168.0.100:8888/"):
    path = os.path.abspath(path.strip())

    print('Search Path:  【{}】  DefaultURL: {}'.format(path, url))

    root = []  # 根目录
    dirs = []  # 文件夹名称
    files = []  # 文件名称
    for root_i, dirs_i, files_i in os.walk(path, topdown=True):
        root.append(root_i)
        dirs.append(dirs_i)
        files.append(files_i)

    # 文件夹大小
    folder_size = 0
    # 文件总数量
    files_num = 0

    for i, root_i in enumerate(root):
        # 当前层次级别
        diff_layer = len(root_i.split(os.sep)) - len(path.split(os.sep)) + 1

        # 非末层文件夹
        if diff_layer < display_layer:
            print(u'{}└-- {}'.format('    ' * (diff_layer - 1), root_i))
            print(u'{} {}'.format('    ' * (diff_layer - 1), url + 'tree/' + '/'.join(root_i.split('/')[2:])))

        # 末层文件夹
        elif diff_layer == display_layer:
            f_num, f_size = _get_folder_size(root_i)
            folder_size += f_size
            files_num += f_num
            print(u'{}└-- {}   【FileNum:{}  Size:{}】'.
                  format('    ' * (diff_layer - 1), root_i, f_num, _size_h(f_size)))
            print(u'{} {}'.format('    ' * (diff_layer - 1), url + 'tree/' + '/'.join(root_i.split('/')[2:])))

        # 文件信息
        if diff_layer < display_layer:
            files_size = 0
            for file_i in files[i]:
                files_size += os.path.getsize(os.path.join(root_i, file_i))
            folder_size += files_size
            files_num += len(files[i])

            if len(files[i]) > 1:
                print("{} ps: {}  ... 【FileNum:{}  Size:{}】".
                      format('    ' * diff_layer, "  ".join(sorted(files[i])[:1]), len(files[i]), _size_h(files_size)))
            elif len(files[i]) > 0:
                print("{} ps: {}      【FileNum:{}  Size:{}】".
                      format('    ' * diff_layer, "  ".join(sorted(files[i])[:1]), len(files[i]), _size_h(files_size)))

    print('\n{}  FileNum:【{}】 Folder Size:【{}】'.format(path, files_num, _size_h(folder_size)))


# 打印指定路径下的 各文件路径 
def print_file_info(path='.', display_num=100, url="http://192.168.0.100:8888/"):
    path = os.path.abspath(path.strip())
    num = 0
    for file_i in sorted(os.listdir(path)):
        if os.path.isfile(os.path.abspath(os.path.join(path, file_i))):
            print("File:{}   Size:{}".format(file_i, _size_h(os.path.getsize(os.path.join(path, file_i)))))

            if file_i.endswith((".jpg", ".png", ".JPG", ".PNG")):
                print(url + 'view/' + '/'.join(os.path.abspath(os.path.join(path, file_i)).split('/')[2:]))
            else:
                print(url + 'edit/' + '/'.join(os.path.abspath(os.path.join(path, file_i)).split('/')[2:]))

            if num >= display_num:
                break
            num += 1

if __name__ == '__main__':
    # print_folder_info(r"D:\Desktop\Gadget")
    print_file_info(r"D:\Desktop\Gadget")
