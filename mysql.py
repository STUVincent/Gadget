# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
MySQL 主要的一些常用操作
调用包： pymysql、prettytable(可视化)

# 当前项目: MySQL_python
# 创建时间: 2018/10/7 21:50
# 开发作者: Vincent
# 创建平台: PyCharm Community Edition    python 3.5
# 版    本: V1.0
"""
import pymysql
from prettytable import PrettyTable


# 数据库操作类
class MySQL:
    # 初始化 连接数据库
    def __init__(self, host, port, user, password, database):
        """
        :param host:     数据库IP地址
        :param port:     数据库端口
        :param user:     用户名
        :param password: 用户密码
        :param database: 数据库名称
        """
        # 打开数据库连接
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        print('Connection Successful.  Database Version: < {} >'.format(self.select_sql("SELECT VERSION();")[0][0]))

    # select 原代码 查询
    def select_sql(self, sql_code):
        """
        :param sql_code:   SQL 查询代码
        :return:  返回所有查询结果
        """
        try:
            # 使用 execute()  方法执行 SQL 查询
            self.cursor.execute(sql_code)
            return self.cursor.fetchall()
        except Exception as error:
            return 'Error: \n{}\n{}'.format(sql_code, error)

    # execute方法执行
    def execute(self, sql_code):
        try:
            self.cursor.execute(sql_code)
            return 'Success:\n{}\nEXECUTE Successfully!'.format(sql_code)
        except Exception as error:
            return 'Error:\n{}\nEXECUTE Error: {}'.format(sql_code, error)

    # 查询数据表结构
    def desc_table(self, table_name=None):
        """
        :param table_name:  待查询的表格名称，若为 None 则循环查询数据库中所有表格的数据结构
        :return:
        """
        if table_name is None:
            table_name = [table_i[0] for table_i in self.select_sql("SHOW TABLES;")]
        else:
            table_name = [table_name]

        table_info = ''
        for table_name_i in table_name:
            sql_code = "DESC {}".format(table_name_i)  # Field  Type  Null  Key  Default  Extra

            # 打印表格信息
            table = PrettyTable()
            table.field_names = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            table.align["Field"] = "l"
            table.padding_width = 1    # 打印表格信息

            for t_i in self.select_sql(sql_code):
                table.add_row(t_i)

            # 查询记录数量
            count = self.select_sql('SELECT COUNT(*) FROM {};'.format(table_name_i))
            # 当前表格数据结构
            table_info_i = 'Table < {} >  Count: < {} >  Information:\n{}'.format(table_name_i, count[0][0], table)
            # 合并到所有表格数据结构信息中
            table_info = '{}\n{}\n'.format(table_info, table_info_i)

        return table_info

    # SQL 创建表格
    def create_table(self, table_name, table_info):
        """
        :param table_name:   创建表格名称
        :param table_info:   创建表格各列信息
        :return:
        """
        sql_code = 'CREATE TABLE {} ({});'.format(table_name, table_info)

        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            # 提交到数据库执行
            self.db.commit()
            return 'Success:\n{}\nCREATE Successfully!'.format(sql_code)
        except Exception as error:
            # 如果发生错误则回滚
            self.db.rollback()
            return 'Error:\n{}\nCREATE Error: {}'.format(sql_code, error)

    # 删除表格
    def drop_table(self, table_name):
        sql_code = 'DROP TABLE {};'.format(table_name)

        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            # 提交到数据库执行
            self.db.commit()
            return 'Success:\n{}\nDROP TABLE Successfully!'.format(sql_code)
        except Exception as error:
            # 如果发生错误则回滚
            self.db.rollback()
            return 'Error:\n{}\nDROP TABLE Error: {}'.format(sql_code, error)

    # SQL 插入数据
    def insert(self, table_name, values, keys=None):
        """
        :param table_name:  表格名称
        :param values:      列值 单条记录：[V1,V2,V3]    多条记录：[[V1,V2,V3],[V1,V2,V3],[V1,V2,V3]]
        :param keys:        列名【若为None，则写入所有的列中】
        :return:
        """
        # 插入多条记录标志
        if isinstance(values[0], (list, tuple)):
            # 将数值合并成SQL CODE
            values_code = ''
            for values_i in values:
                values_code_j = ''
                for values_i_j in values_i:
                    if isinstance(values_i_j, (int, float)) or values_i_j in ('NOW()', 'CURTIME()'):
                        values_code_j += "{},".format(values_i_j)
                    elif values_i_j is None:
                        values_code_j += "'{}',".format(values_i_j)
                    else:
                        values_code_j += "{},".format(repr(values_i_j))
                values_code += "({}),".format(values_code_j[: -1])

            if keys is None:
                sql_code = "INSERT INTO {} VALUES {};".format(table_name, values_code[: -1])
            else:
                sql_code = "INSERT INTO {} ({}) VALUES {};".format(table_name, ",".join(keys), values_code[: -1])

        # 插入单条记录
        else:
            # 将数值合并成SQL CODE
            values_code = ''
            for values_i in values:
                if isinstance(values_i, (int, float)) or values_i in ('NOW()', 'CURTIME()'):
                    values_code += "{},".format(values_i)
                elif values_i is None:
                    values_code += "'{}',".format(values_i)
                else:
                    values_code += "{},".format(repr(values_i))

            if keys is None:
                sql_code = "INSERT INTO {} VALUES ({});".format(table_name, values_code[: -1])
            else:
                sql_code = "INSERT INTO {} ({}) VALUES ({});".format(table_name, ",".join(keys), values_code[: -1])

        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            # 提交到数据库执行
            self.db.commit()
            return 'Success:\n{}\nINSERT Successfully!'.format(sql_code)
        except Exception as error:
            # 如果发生错误则回滚
            self.db.rollback()
            return 'Error:\n{}\nINSERT Error: {}'.format(sql_code, error)

    # SQL 更新数据
    def update(self, table_name, update_code, condition_code):
        """
        :param table_name:      更新表格名称
        :param update_code:     更新数值语句
        :param condition_code:  更新条件语句
        :return:
        """
        sql_code = 'UPDATE {} SET {} WHERE {};'.format(table_name, update_code, condition_code)
        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            # 提交到数据库执行
            self.db.commit()
            return 'Success:\n{}\nUPDATE Successfully!'.format(sql_code)
        except Exception as error:
            # 如果发生错误则回滚
            self.db.rollback()
            return 'Error:\n{}\nUPDATE Error: {}'.format(sql_code, error)

    # SQL 删除数据
    def delete(self, table_name, condition_code):
        """
        :param table_name:      表格名称
        :param condition_code:  删除条件语句
        :return:
        """
        sql_code = 'DELETE FROM {} WHERE {};'.format(table_name, condition_code)
        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            # 提交到数据库执行
            self.db.commit()
            return 'Success:\n{}\nDELETE Successfully!'.format(sql_code)
        except Exception as error:
            # 如果发生错误则回滚
            self.db.rollback()
            return 'Error:\n{}\nDELETE Error: {}'.format(sql_code, error)

    # SQL 查询数据
    def select(self, table_name, keys=None, condition_code=None, string_flag=False):
        """
        :param table_name:     查询表格名称
        :param keys:           查询列名，若为None 默认查询所有列
        :param condition_code: 查询条件，若为None 默认查询所有数据
        :param string_flag:    是否以字符串形式输出，True时，通过Prettytable 显示为表格数据
        :return:
        """
        if keys is None:
            key_code = '*'
        else:
            key_code = ','.join(keys)

        if condition_code is None:
            sql_code = "SELECT {} FROM {};".format(key_code, table_name)
        else:
            sql_code = "SELECT {} FROM {} WHERE {};".format(key_code, table_name, condition_code)

        try:
            # 执行sql语句
            self.cursor.execute(sql_code)
            select_data = self.cursor.fetchall()

            # 转换成表格方便可视化
            if string_flag:
                # 打印表格信息
                table = PrettyTable()
                if keys is None:
                    table.field_names = [columns[0] for columns in self.select_sql("DESC {}".format(table_name))]
                else:
                    table.field_names = keys

                table.align["Field"] = "l"
                table.padding_width = 1    # 打印表格信息

                for s_i, select_data_i in enumerate(select_data):
                    table.add_row(select_data_i)
                    # 默认只显示指定行数 17+2
                    if s_i > 17:
                        table.add_row(['.']*len(select_data[0]))
                        break

                select_data = 'Table < {} >  Count: < {} >  Values:\n{}\n'.format(
                    table_name, len(select_data), table)

            return select_data

        except Exception as error:
            return 'Error:\n{}\nSELECT Error: {}'.format(sql_code, error)

    # 关闭数据库连接
    def close(self):
        # 关闭cursor
        self.cursor.close()
        # 关闭数据库
        self.db.close()


if __name__ == '__main__':

    # 打开数据库连接
    # db = MySQL(host='192.169.0.0', port=3306, user='vincent', password='vincent', database="demo")

    # 初始化数据库
    if True:
        # 删除数据库中已有表格
        for table_j in db.select_sql("SHOW TABLES;"):
            print(db.drop_table(table_j[0]))

        # 创建表格
        table_information = ["ID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT",  # ID 主键 自增1
                             "NAME CHAR(20) NOT NULL",
                             "AGE TINYINT UNSIGNED",
                             "SEX CHAR(1) DEFAULT 'M'",
                             "INCOME FLOAT",
                             "TIME DATETIME",
                             "STRING VARCHAR(20)"
                             ]
        print(db.create_table('table_demo', ','.join(table_information)))

        # 插入数据
        table_keys = ['NAME', 'AGE', 'INCOME', 'TIME', 'STRING']
        table_values = [('Mac', 15, 8000, 'NOW()', None),
                        ('Vincent', 25, 28000, 'NOW()', ',"a "daf " '),
                        ('And', 25, 28000, 'NOW()', ",daf{}'}"),
                        ('A2', 25, 28000, 'NOW()', "("),
                        ('A#', 25, 28000, 'NOW()', "}"),
                        ('A@', 25, 28000, 'NOW()', ",')],"),
                        ('Viky', 18, 1.2, 'NOW()', '""".')]
        # for table_values_i in table_values:
        #     print(db.insert('table_demo', values=table_values_i, keys=table_keys))

        print(db.insert('table_demo', values=table_values, keys=table_keys))

        # 当前最大 ID 值
        # print(db.select_sql('SELECT LAST_INSERT_ID()'))
        max_id = db.select_sql('SELECT MAX(ID) FROM table_demo')[0][0]

        print(db.insert('table_demo', values=(max_id+1, '中国', 20, 'F', 1000, 'NOW()', 'demo')))

    # 打印表格字典
    print(db.desc_table())

    max_id = db.select_sql('SELECT MAX(ID) FROM table_demo')[0][0]

    print(db.insert('table_demo', values=(max_id+1, '中国', 20, 'F', 1000, 'NOW()', None)))

    print(db.select("table_demo", string_flag=True))

    # # 更新数据
    # print(db.update("table_demo", "INCOME=999", "NAME='Viky'"))
    # # 删除数据
    # print(db.delete("table_demo", "INCOME>20000"))
    # # 查询数据
    # print(db.select("table_demo", string_flag=True))
    # print(db.select("table_demo", condition_code="SEX='M'", keys=('AGE', 'NAME', 'SEX')))

    while False:
        input_code = input('请输入查询条件： table_name, key_list, condition\n')
        if input_code in ('q', 'Q'):
            break

        input_data = input_code.split(',')
        if len(input_data) == 3:
            # print(input_data)

            if len(input_data[1].strip()) > 0:
                keys_list = input_data[1].split()
            else:
                keys_list = None

            if len(input_data[2].strip()) > 0:
                condition = input_data[2].strip()
            else:
                condition = None

            print(db.select(input_data[0], keys=keys_list, condition_code=condition, string_flag=True))

        else:
            print('输入有误，请重新输入\n')

    # 关闭数据库连接
    db.close()
