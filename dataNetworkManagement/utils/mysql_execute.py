#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymysql
from dataNetworkManagement.utils.get_yaml_datas import GetYamlDatas


class MysqlExecute():

    def mysql_execute(self, sql):
        """
        连接数据库并执行sql语句
        :param sql:
        :return:
        """
        try:
            # 定义数据库连接
            mysql_connect = pymysql.connect(user=GetYamlDatas().get_yaml_datas()['mysql_hz_prod']['username'],
                                            password=GetYamlDatas().get_yaml_datas()['mysql_hz_prod']['password'],
                                            host=GetYamlDatas().get_yaml_datas()['mysql_hz_prod']['host'],
                                            port=GetYamlDatas().get_yaml_datas()['mysql_hz_prod']['port'])
            # 创建一个数据库游标
            mysql_cursor = mysql_connect.cursor()
            # 使用游标来执行sql语句
            mysql_cursor.execute(sql)
            # 关闭数据库连接
            mysql_cursor.close()
            if "select" in sql:
                # 获取执行sql之后的结果
                mysql_execute_result = mysql_cursor.fetchall()
                # 返回获取到的结果
                return mysql_execute_result
            elif "delete" in sql:
                mysql_connect.commit()
            else:
                pass
        except pymysql.err.OperationalError as pymysql_error:
            print(f"数据库连接失败，失败信息：{pymysql_error}")


# a = MysqlExecute().mysql_execute(
#     f"select * from data_network_prod.d_data_manager_info where name = 'Data_name_http_add_auto_test'")
# print(a)
