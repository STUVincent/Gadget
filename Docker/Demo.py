# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
# 当前项目: ChinaHadoop_C03-master
# 创建时间: 2019/1/27 21:59 
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
import os
import argparse
import time


# 输入参数设置、全局参数、日志初始化
def argument_init():
    # ############################ CMD 传参 ################################################
    parser = argparse.ArgumentParser(
        description="""
        Demo 代码

        ..............................................................................
        """,
        epilog="""
        ..............................................................................
        End help!  author:Vincent  2019-1-27
        """)

    # required  参数是否为必须项[True|False]
    # nargs=     '+' 至少传入一个参数    '*' 传入0个或多个参数
    # default   默认值
    # help      帮助信息
    # type      参数属性默认都是字符串 [int|float|str]
    # choices   可选项 ['rock', 'paper', 'scissors']

    # 当前程序版本
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='the version of this code')

    # 输入文件夹
    parser.add_argument('--InputPath', default='/InputPath', help='输入文件夹')

    # 输出文件夹
    parser.add_argument('--OutputPath', default='/OutputPath', help='输出文件夹')

    # InputCommand
    parser.add_argument('--input_string', default='Default', help="InputCommand")

    args = parser.parse_args()

    # 开始时间 浮点型
    args.Start_time_float = time.time()
    # 开始时间 字符型
    args.Start_time_str = time.strftime('%Y%m%d%H%M%S', time.localtime())

    # 当前目录路径
    args.CWD = os.path.abspath(os.path.dirname(__file__))

    # ############################# 打印参数 ################################################
    # 读取 args 中的所有参数
    args_info = args.__dict__
    print('{}{:20s}{}'.format('* '*15, "     Arguments    ", '* '*15))
    for i, args_i in enumerate(sorted(args_info)):
        print('args_{:02d} ---  {:s} : {}'.format(i+1, args_i, args_info[args_i]))
    print('{}'.format('* '*40))

    if args.InputPath is not None:
        print("InputPath : ", os.listdir(args.InputPath))
    if args.OutputPath is not None:
        print("OutputPath: ", os.listdir(args.OutputPath))

    return args


if __name__ == '__main__':
    argument_init()
